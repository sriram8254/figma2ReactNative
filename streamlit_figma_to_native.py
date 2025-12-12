# app.py


import streamlit as st
import os
import re
import tempfile
import zipfile
import time
from google import genai
from io import BytesIO
import sys
import pandas as pd
from pathlib import Path


# Import both prompts from one clean file
from prompts import GENERATE_PROMPT, ENRICH_PROMPT


# ====================== .ENV PARSING FUNCTION ======================


def parse_env_file(env_path):
    """Parse .env file and return dictionary of key-value pairs"""
    env_vars = {}
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                # Split on first '=' only
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present (handles both ' and ")
                    if value and value[0] in ['"', "'"] and value[-1] in ['"', "'"]:
                        value = value[1:-1]
                    
                    # Remove 'r' prefix if present (from raw strings)
                    if value.startswith("r'") or value.startswith('r"'):
                        value = value[2:-1]
                    
                    # Normalize Windows paths (convert backslashes to forward slashes)
                    if '\\' in value:
                        value = value.replace('\\\\', '/').replace('\\', '/')
                    
                    env_vars[key] = value
        return env_vars
    except Exception as e:
        st.error(f"Error parsing .env file: {e}")
        return {}


def load_file_from_path(file_path):
    """Load file content from given path"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            st.warning(f"File not found: {file_path}")
            return None
    except Exception as e:
        st.error(f"Error loading file {file_path}: {e}")
        return None


# ====================== MASKING & COMMENT REMOVAL FUNCTIONS ======================


def mask_word(text: str, old: str = "GIB", new: str = "ABC") -> str:
    """Replace 'GIB' (any case) with 'ABC' safely – avoids partial word matches in most cases"""
    if not old or not text:
        return text


    # Normalize old word
    old_lower = old.lower()


    # Build regex: matches the word in any case
    pattern = re.compile(re.escape(old), re.IGNORECASE)


    def replace(match):
        matched = match.group(0)
        start, end = match.start(), match.end()


        before_char = text[start-1] if start > 0 else ""
        after_char = text[end] if end < len(text) else ""


        # Only apply strict safety for short words (3–5 letters)
        if (before_char.isalpha() and before_char.islower()) and \
           (after_char.isalpha() and after_char.islower()):
            return matched  # ← block "eligible", "GIBbing"


        # For longer sequences (gibretailing, GIBRetailMobile), always replace
        if matched.isupper():
            return new.upper()
        elif matched.islower():
            return new.lower()
        elif matched[0].isupper():
            return new.capitalize()
        else:
            return new.capitalize()


    return pattern.sub(replace, text)


def remove_comments_from_code(content: str) -> str:
    """Remove //, /* */, and {/** */} comments + clean empty lines"""


    original_content = content


    # Remove JSX-style {/** */} comments
    content = re.sub(r'\{/\*.*?\*/\}', '', content, flags=re.DOTALL)


    # Remove standard /* */ comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)


    lines = content.split('\n')
    cleaned_lines = []


    for line in lines:
        if '//' in line:
            in_string = False
            string_char = None
            comment_pos = -1


            for i, char in enumerate(line):
                if char in ['"', "'", '`'] and (i == 0 or line[i-1] != '\\'):
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                        string_char = None


                if not in_string and i < len(line) - 1 and line[i:i+2] == '//':
                    comment_pos = i
                    break


            if comment_pos != -1:
                line = line[:comment_pos].rstrip()


        cleaned_lines.append(line)


    content = '\n'.join(cleaned_lines)


    # Remove excessive blank lines
    lines = content.split('\n')
    cleaned_lines = []
    prev_empty = False


    for line in lines:
        is_empty = line.strip() == ''


        if not is_empty:
            cleaned_lines.append(line)
            prev_empty = False
        elif not prev_empty:
            cleaned_lines.append(line)
            prev_empty = True


    content = '\n'.join(cleaned_lines)


    return content


# ====================== CONFIG ======================
st.set_page_config(page_title="Figma to React Native Converter", layout="wide", page_icon="📱")


st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
    }
    .tab-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        padding: 0.5rem 1.8rem;
        font-weight: bold;
    }
    .image-grid {display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;}
    .image-item {flex: 0 0 calc(33.333% - 10px); text-align: center;}
</style>
""", unsafe_allow_html=True)


st.markdown(
    "<div class='main-header'><h1>📱 Figma to React Native Converter</h1>    "
    "<p style=\"font-size: 1.1em; margin-top: 1rem;\">Transform your Figma designs into production-ready React Native components with AI-powered analysis</p></div>",
    unsafe_allow_html=True
)


# Session state initialization - EXPANDED
session_keys = {
    "api_key": "",
    "components": [],
    "selected_components": [],
    "folder_path": "",
    "mapping_text": "",
    "component_df": None,
    "generated": "",
    "enriched": "",
    "figma_imgs_tab1": [],
    "figma_imgs_tab2": [],
    "conventions_content": "",
    "theme_content": "",
    "additional_context": "FeatureName:\nScreenName(ViewName):\nAdditionalContext:",
}


for key, default_value in session_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


# ====================== SIDEBAR WITH .ENV LOADER ======================


with st.sidebar:
    st.header("⚙️ Configuration")
    
    # .ENV file path input
    env_file_path = st.text_input(
        "📄 .env File Path",
        placeholder="Enter path to .env file",
        help="Load API key and file paths from .env file"
    )
    
    if st.button("Load .env File") and env_file_path:
        if os.path.exists(env_file_path):
            env_vars = parse_env_file(env_file_path)
            
            if env_vars:
                # Load API Key
                if "API_KEY" in env_vars:
                    st.session_state.api_key = env_vars["API_KEY"]
                
                # Load Conventions & Standards
                if "CONVENTIONS_PATH" in env_vars:
                    content = load_file_from_path(env_vars["CONVENTIONS_PATH"])
                    if content:
                        st.session_state.conventions_content = content
                
                # Load Sample Code
                if "SAMPLE_CODE_PATH" in env_vars:
                    content = load_file_from_path(env_vars["SAMPLE_CODE_PATH"])
                    if content:
                        st.session_state["sample_code_content"] = content
                
                # Load Package Structure
                if "PACKAGE_STRUCTURE_PATH" in env_vars:
                    content = load_file_from_path(env_vars["PACKAGE_STRUCTURE_PATH"])
                    if content:
                        st.session_state["package_structure_content"] = content
                
                # Load Theme Configuration
                if "THEME_CONFIG_PATH" in env_vars:
                    content = load_file_from_path(env_vars["THEME_CONFIG_PATH"])
                    if content:
                        st.session_state.theme_content = content
                
                # Load Components Folder Path
                if "COMPONENTS_FOLDER_PATH" in env_vars:
                    st.session_state.folder_path = env_vars["COMPONENTS_FOLDER_PATH"]
                
                # Load API Endpoints
                if "API_ENDPOINTS_PATH" in env_vars:
                    content = load_file_from_path(env_vars["API_ENDPOINTS_PATH"])
                    if content:
                        st.session_state["api_endpoints_content"] = content
                
                st.success("✅ .env file loaded successfully!")
        else:
            st.error("❌ .env file not found!")
    
    st.markdown("---")
    
    # API Key input (can be overridden manually)
    api_key = st.text_input(
        "🔑 Google Gemini API Key",
        type="password",
        placeholder="Enter your Google Gemini API Key",
        value=st.session_state.api_key,
        help="Get your key from https://aistudio.google.com/app/apikey"
    )
    st.session_state.api_key = api_key


# ====================== CLEAN HELPERS ======================


def remove_blank_lines(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if line.strip())


def compact_json(text: str) -> str:
    lines = []
    prev_blank = False
    for line in text.splitlines():
        is_blank = not line.strip()
        if is_blank and prev_blank:
            continue
        lines.append(line)
        prev_blank = is_blank
    return '\n'.join(lines)


def split_large_file(file_content, lines_per_chunk=8500):
    compacted = compact_json(file_content)
    lines = compacted.splitlines(keepends=True)
    return ["".join(lines[i:i + lines_per_chunk]) for i in range(0, len(lines), lines_per_chunk)]


def merge_components(base_path, folders):
    result = ""
    for folder in folders:
        path = os.path.join(base_path, folder)
        if not os.path.isdir(path):
            continue
        result += f"\n// COMPONENT: {folder}\n"
        for root, _, files in os.walk(path):
            if "assets" in os.path.basename(root):
                continue
            for file in files:
                if file.endswith(('.tsx', '.ts', '.js', '.jsx')):
                    fp = os.path.join(root, file)
                    rel = os.path.relpath(fp, base_path).replace("\\", "/")
                    try:
                        with open(fp, 'r', encoding='utf-8') as f:
                            content = "\n".join(l for l in f.read().splitlines() if l.strip())
                            result += f"// {rel}\n{content}\n\n"
                    except Exception:
                        pass
    return result


# ====================== TABS ======================
tab1, tab2, tab3 = st.tabs(["🎨 Generate Code", "✨ Enhance Styling", "📦 Export Project"])


# ====================== TAB 1: Generate Code ======================
with tab1:
    st.markdown("""
<div class="tab-header">
    <h3> 🎨 Generate React Native Code from Figma</h3>
    <p>Upload Figma images along with conventions, user stories, Sample Code, Package Structure, and API Endpoints files to generate complete React Native code.</p>
</div>
""", unsafe_allow_html=True)


    col1, col2 = st.columns([1, 2])


    with col1:
        st.subheader("Screen Specific Inputs")
        figma_imgs = st.file_uploader(
            "📸 Figma Design(s)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="figma_tab1",
            help="You can upload multiple screens/flow images"
        )


        if figma_imgs:
            st.success(f"Uploaded {len(figma_imgs)} image(s)")
            st.session_state.figma_imgs_tab1 = figma_imgs
            cols = st.columns(3)
            for idx, img in enumerate(figma_imgs):
                cols[idx % 3].image(img, width=180, caption=img.name.split('.')[0])


    with col2:
        
        user_stories = st.file_uploader("📋 User Stories", type=["json", "txt"])
        
        # API Endpoints file upload
        api_endpoints_file = st.file_uploader(
            "🔌 API Endpoints",
            type="txt",
            help="Upload API endpoints file with endpoint definitions, request/response schemas, and examples"
        )
        
        # Show loaded content from .env if available
        if "api_endpoints_content" in st.session_state and st.session_state["api_endpoints_content"] and not api_endpoints_file:
            st.info("✅ API Endpoints loaded from .env file")


        # Optional Component Mapping upload
        component_mapping_file = st.file_uploader(
            "🧩 Optional: Component Mapping (CSV/XLSX)",
            type=["csv", "xlsx"],
            help="3 cols: Component-Folder Name, Component Name, Mapping"
        )


        if component_mapping_file is not None:
            try:
                if component_mapping_file.name.lower().endswith(".csv"):
                    df = pd.read_csv(component_mapping_file)
                else:
                    df = pd.read_excel(component_mapping_file)
                # Ensure at least 3 columns; rename first three for clarity
                if df.shape[1] >= 3:
                    df = df.iloc[:, :3]
                    df.columns = ["Component-Folder Name", "Component Name", "Mapping"]
                else:
                    st.warning("Component mapping file must have at least 3 columns.")
                    df = None
            except Exception as e:
                st.error(f"Error reading mapping file: {e}")
                df = None


            st.session_state.component_df = df
        else:
            # If file is removed/not uploaded, reset to None
            st.session_state.component_df = None

        # ============ NEW: EXPANDER FOR GROUPED FILES ============
        with st.expander("📁 Common Input Files", expanded=False):
            conventions_file = st.file_uploader(
                "📐 Conventions & Standards",
                type="txt",
                help="Upload conventions_and_standards.txt file with naming conventions, import rules, typography patterns, etc."
            )
            
            # Show loaded content from .env if available
            if st.session_state.conventions_content and not conventions_file:
                st.info("✅ Conventions loaded from .env file")
            
            sample_code = st.file_uploader("📄 Sample Code", type="txt")
            
            # Show loaded content from .env if available
            if "sample_code_content" in st.session_state and st.session_state["sample_code_content"] and not sample_code:
                st.info("✅ Sample Code loaded from .env file")
            
            package_json = st.file_uploader("📦 Package Structure", type=["json", "txt"])
            
            # Show loaded content from .env if available
            if "package_structure_content" in st.session_state and st.session_state["package_structure_content"] and not package_json:
                st.info("✅ Package Structure loaded from .env file")
        
        # ============ END EXPANDER ============


    st.markdown("---")
    folder = st.text_input("📁 Existing Components Folder:", value=st.session_state.folder_path)
    if st.button("Load Components") and folder and os.path.exists(folder):
        st.session_state.folder_path = folder
        st.session_state.components = sorted(
            [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
        )
        st.success(f"Loaded {len(st.session_state.components)} components")


    if st.session_state.components:
        search = st.text_input("Search components:", key="search1")
        filtered = [c for c in st.session_state.components if search.lower() in c.lower()]


        cols = st.columns(5)
        sel = st.session_state.selected_components.copy()


        # If mapping file exists, build a set of component names from first column
        mapped_names = set()
        if st.session_state.component_df is not None and "Component-Folder Name" in st.session_state.component_df.columns:
            mapped_names = {
                str(x).strip()
                for x in st.session_state.component_df["Component-Folder Name"].dropna().tolist()
            }


        for i, c in enumerate(filtered):
            was = c in sel


            # Default checkbox value:
            default_checked = was
            # If mapping exists and current component name appears in first column,
            # then preselect it
            if mapped_names and c in mapped_names and not was:
                default_checked = True


            now = cols[i % 5].checkbox(c, value=default_checked, key=f"cb1_{c}")


            if now and c not in sel:
                sel.append(c)
            if not now and c in sel:
                sel.remove(c)


        st.session_state.selected_components = sel


        if sel:
            st.markdown(
                f"<div class='success-box'>Selected ({len(sel)}): {', '.join(sel)}</div>",
                unsafe_allow_html=True
            )


            # ============ CONDITIONAL DISPLAY: TABLE OR TEXT AREA ============
            if st.session_state.component_df is not None:
                # SCENARIO 2: Show editable table (full width)
                st.markdown("### 🗂️ Component Mapping Table (editable)")
                edited_df = st.data_editor(
                    st.session_state.component_df,
                    num_rows="dynamic",
                    width='stretch',
                    key="component_mapping_editor"
                )
                st.session_state.component_df = edited_df
                
                # NEW: Additional context text area below table
                st.markdown("### 📝 Additional Context")
                additional_context = st.text_area(
                    "Additional information for the mapping:",
                    value=st.session_state.additional_context,
                    height=150,
                    key="additional_context_tab1"
                )
                st.session_state.additional_context = additional_context
                
            else:
                # SCENARIO 1: Show text area (old behavior)
                default_lines = ["Feature:", "Screen Name:", "Component Name"]
                default_lines += [f"{c} -" for c in sel]
                default_lines += ["AdditionalContext:", ""]


                if len(sel) != len(
                    [l for l in st.session_state.mapping_text.splitlines() if l.endswith(" -")]
                ):
                    st.session_state.mapping_text = "\n".join(default_lines)


                mapping = st.text_area(
                    "🗺️ Component Mapping:",
                    st.session_state.mapping_text,
                    height=300
                )
                st.session_state.mapping_text = mapping


    if st.button("Generate Code", type="primary"):
        if not st.session_state.api_key:
            st.error("Please enter your Gemini API key in the sidebar")
        elif not figma_imgs:
            st.error("Please upload at least one Figma image")
        else:
            # Check for conventions - either from upload or .env
            has_conventions = conventions_file or st.session_state.conventions_content
            if not has_conventions:
                st.error("Please upload the Conventions & Standards file or load from .env")
            else:
                with st.spinner("Generating code using Gemini..."):
                    client = genai.Client(api_key=st.session_state.api_key)


                    # Read conventions - prioritize uploaded file, fallback to .env
                    if conventions_file:
                        conventions_content = remove_blank_lines(conventions_file.read().decode())
                    else:
                        conventions_content = remove_blank_lines(st.session_state.conventions_content)


                    merged = merge_components(
                        st.session_state.folder_path,
                        st.session_state.selected_components
                    ) if st.session_state.selected_components else ""


                    user_stories_txt = remove_blank_lines(user_stories.read().decode()) if user_stories else "None"
                    
                    # Sample code - prioritize upload, fallback to .env
                    if sample_code:
                        sample_code_txt = remove_blank_lines(sample_code.read().decode())
                    elif "sample_code_content" in st.session_state and st.session_state["sample_code_content"]:
                        sample_code_txt = remove_blank_lines(st.session_state["sample_code_content"])
                    else:
                        sample_code_txt = "None"
                    
                    # Package structure - prioritize upload, fallback to .env
                    if package_json:
                        package_txt = remove_blank_lines(package_json.read().decode())
                    elif "package_structure_content" in st.session_state and st.session_state["package_structure_content"]:
                        package_txt = remove_blank_lines(st.session_state["package_structure_content"])
                    else:
                        package_txt = "None"
                    
                    # API endpoints - prioritize upload, fallback to .env
                    if api_endpoints_file:
                        api_endpoints_txt = remove_blank_lines(api_endpoints_file.read().decode())
                    elif "api_endpoints_content" in st.session_state and st.session_state["api_endpoints_content"]:
                        api_endpoints_txt = remove_blank_lines(st.session_state["api_endpoints_content"])
                    else:
                        api_endpoints_txt = "None"


                    # ============ BUILD MAPPING CONTENT ============
                    sel = st.session_state.selected_components or []
                    df_map = st.session_state.component_df


                    if df_map is not None and "Component-Folder Name" in df_map.columns:
                        # SCENARIO 2: Build from table - USE ALL ROWS (NO FILTERING)
                        lines = ["Feature:", "Screen Name:", "Component Name"]
                        
                        for _, row in df_map.iterrows():
                            name = str(row.get("Component-Folder Name", "")).strip()
                            label = str(row.get("Component Name", "")).strip()
                            extra = str(row.get("Mapping", "")).strip()
                            
                            # Only skip if name is empty
                            if not name:
                                continue
                            
                            # Format: Component-Folder Name | Component Name | Mapping
                            line_parts = [name]
                            if label:
                                line_parts.append(label)
                            if extra:
                                line_parts.append(extra)
                            
                            lines.append(" | ".join(line_parts))
                        
                        # Append additional context
                        lines.append("\n" + st.session_state.additional_context)
                        mapping = "\n".join(lines)
                    else:
                        # SCENARIO 1: Use text area content
                        mapping = st.session_state.mapping_text


                    # Substitute all placeholders including api_endpoints
                    prompt = GENERATE_PROMPT.replace("{conventions_and_standards}", conventions_content) \
                        .replace("{component_mapping}", mapping) \
                        .replace("{existing_components}", merged) \
                        .replace("{user_stories_file_content}", user_stories_txt) \
                        .replace("{sample_code}", sample_code_txt) \
                        .replace("{package_structure}", package_txt) \
                        .replace("{api_endpoints}", api_endpoints_txt)


                    # APPLY GIB MASKING BEFORE HITTING LLM
                    prompt = mask_word(prompt)


                    try:
                        prompt_save_path = r"C:\Solutions\figma user story trial\output_folder\gib_mobile\st_check_multi_figma.txt"
                        os.makedirs(os.path.dirname(prompt_save_path), exist_ok=True)
                        with open(prompt_save_path, "w", encoding="utf-8", errors="ignore") as f:
                            f.write(prompt)
                        print(f"✅ PROMPT SAVED: {prompt_save_path}")
                    except Exception as e:
                        print(f"❌ PROMPT SAVE ERROR: {str(e)}")


                    # Build content: images first, then prompt
                    contents = []
                    for img in figma_imgs:
                        contents.append(genai.types.Part.from_bytes(data=img.read(), mime_type=img.type))
                        img.seek(0)  # reset for future use
                    contents.append(prompt)


                    resp = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=contents,
                    )
                    st.session_state.generated = resp.text
                    st.success("✅ Code generated successfully!")
                    st.download_button("⬇️ Download Generated Code", resp.text, "generated_code.txt")


# ====================== TAB 2: Enhance Styling ======================
with tab2:
    st.markdown("""
    <div class="tab-header">
        <h3>✨Enhance with Pixel-Perfect Styling</h3>
        <p>Upload Figma image, generated React Native code, Theme Styles and Figma Screen data(extracted using API) to enrich the code with detailed styling information.</p>
    </div>
    """, unsafe_allow_html=True)


    c1, c2 = st.columns([1, 2])


    with c1:
        st.subheader("Screen Specific Inputs")
        
        # Auto-populate from Tab 1
        default_figma_tab2 = st.session_state.figma_imgs_tab1 if st.session_state.figma_imgs_tab1 else None
        
        figma_imgs_enrich = st.file_uploader(
            "📸 Figma Design(s)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="figma_tab2"
        )
        
        # If no new upload and tab1 has images, use them
        if not figma_imgs_enrich and st.session_state.figma_imgs_tab1:
            figma_imgs_enrich = st.session_state.figma_imgs_tab1
            st.info("✅ Using Figma images from Tab 1")
        
        if figma_imgs_enrich:
            st.success(f"Uploaded {len(figma_imgs_enrich)} image(s)")
            cols = st.columns(3)
            for idx, img in enumerate(figma_imgs_enrich):
                cols[idx % 3].image(img, width=180, caption=img.name.split('.')[0])


    with c2:
        theme = st.file_uploader("🎨 Theme Configuration", type=["txt", "json"])
        
        # Show loaded content from .env if available
        if st.session_state.theme_content and not theme:
            st.info("✅ Theme Configuration loaded from .env file")
        
        # Pre-fill generated code from Tab 1
        code_in = st.file_uploader("📄 Generated Code", type="txt", key="code_enrich")
        
        # If no upload but we have generated code from tab1, show info
        if not code_in and st.session_state.generated:
            st.info("✅ Using generated code from Tab 1")
        
        figma_json_file = st.file_uploader("📊 Figma API Data ", type=["json", "txt"], key="figma_json")


    if st.button("✨ Start Enhancement", type="primary"):
        # Determine which code to use
        if code_in:
            current_code = remove_blank_lines(code_in.read().decode())
        elif st.session_state.generated:
            current_code = remove_blank_lines(st.session_state.generated)
        else:
            current_code = None
        
        # Determine which theme to use
        if theme:
            theme_txt = remove_blank_lines(theme.read().decode())
        elif st.session_state.theme_content:
            theme_txt = remove_blank_lines(st.session_state.theme_content)
        else:
            theme_txt = None
        
        required = [st.session_state.api_key, figma_imgs_enrich, theme_txt, current_code, figma_json_file]
        if not all(required):
            st.error("❌ All fields are required!")
        else:
            with st.spinner("⏳ Enhancing styling ..."):
                client = genai.Client(api_key=st.session_state.api_key)


                json_content = figma_json_file.read().decode()


                # Hardcoded lines_per_chunk = 21500
                chunks = split_large_file(json_content, 21500)
                st.info(f"📊 Processing Figma API Json file")


                # Prepare image parts once
                image_parts = [
                    genai.types.Part.from_bytes(data=img.read(), mime_type=img.type)
                    for img in figma_imgs_enrich
                ]
                for img in figma_imgs_enrich:
                    img.seek(0)


                progress_bar = st.progress(0)
                status = st.empty()


                for i, chunk in enumerate(chunks):
                    status.text(f"🔄 Processing code {i+1}/{len(chunks)}...")


                    prompt = ENRICH_PROMPT \
                        .replace("{iteration_number}", str(i+1)) \
                        .replace("{part_number}", str(i+1)) \
                        .replace("{total_parts}", str(len(chunks))) \
                        .replace("{current_code}", current_code) \
                        .replace("{figma_json_chunk}", chunk) \
                        .replace("{theme_colors_content}", theme_txt)


                    # APPLY GIB MASKING BEFORE HITTING LLM
                    prompt = mask_word(prompt)


                    try:
                        prompt_save_path = r"C:\Solutions\figma user story trial\output_folder\gib_mobile\st_check_2_multi_figma.txt"
                        os.makedirs(os.path.dirname(prompt_save_path), exist_ok=True)
                        with open(prompt_save_path, "w", encoding="utf-8", errors="ignore") as f:
                            f.write(prompt)
                        print(f"✅ PROMPT SAVED: {prompt_save_path}")
                    except Exception as e:
                        print(f"❌ PROMPT SAVE ERROR: {str(e)}")


                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=image_parts + [prompt],
                        )
                        current_code = response.text
                        progress_bar.progress((i + 1) / len(chunks))
                        time.sleep(1)
                    except Exception as e:
                        st.error(f"Error in chunk {i+1}: {e}")
                        break


                st.session_state.enriched = current_code
                status.empty()
                st.success("✨ Styling enhancement complete!")
                st.balloons()


    if "enriched" in st.session_state and st.session_state.enriched:
        st.download_button(
            "⬇️ Download Final Enhanced Code",
            st.session_state.enriched,
            "final_enriched_code.txt"
        )


# ====================== TAB 3: Export Project ======================
with tab3:
    st.markdown("""
    <div class="tab-header"> 
        <h3>📁 Create Project Structure</h3>
        <p>Upload generated React Native code file to parse and create a downloadable project folder structure.</p>
    </div>
    """, unsafe_allow_html=True)


    zip_input = st.file_uploader("📄 Generated React Native Code", type="txt", key="zip_input")
    
    # If no upload but we have enriched code from tab2, show info
    if not zip_input and st.session_state.enriched:
        st.info("✅ Using enhanced code from Tab 2")


    # NEW: Radio button for comment handling
    comment_option = st.radio(
        "💬 Comment Handling:",
        options=["Without Comments", "With Comments"],
        index=0,  # Default to "Without Comments"
        horizontal=True,
        help="Choose whether to keep or remove comments in the exported code"
    )


    if st.button("📦 Create ZIP Archive"):
        # Determine which code to use
        if zip_input:
            raw_content = zip_input.read().decode()
        elif st.session_state.enriched:
            raw_content = st.session_state.enriched
        else:
            st.error("❌ No code available. Please upload a file or generate code in previous tabs.")
            raw_content = None


        if raw_content:
            # Apply comment removal based on user selection
            if comment_option == "Without Comments":
                cleaned_content = remove_comments_from_code(raw_content)
            else:
                cleaned_content = raw_content  # Keep comments


            content = cleaned_content  # Use cleaned/original content for ZIP


            with tempfile.TemporaryDirectory() as tmp_dir:
                current_path = None
                lines = []


                def save_file():
                    if current_path and lines:
                        full_path = os.path.join(tmp_dir, current_path)
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write("\n".join(lines))


                for line in content.splitlines():
                    match = re.search(r"###FilePath:\s*(.+)", line)
                    if match:
                        save_file()
                        current_path = match.group(1).strip()
                        lines = []
                    elif not line.strip().startswith("```"):
                        lines.append(line.rstrip())
                save_file()


                buffer = BytesIO()
                with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
                    for root, _, files in os.walk(tmp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arc_name = os.path.relpath(file_path, tmp_dir)
                            z.write(file_path, arc_name)
                buffer.seek(0)


                st.download_button(
                    "📥 Download Project ZIP",
                    buffer,
                    "react_native_project.zip",
                    "application/zip"
                )
                st.success("✅ Project archive created successfully!")


# ====================== FOOTER ======================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 2rem; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
    <h4 style="color: #495057; margin-bottom: 1rem;">🎨 Figma to React Native Code Generator</h4>
    <p style="color: #6c757d; margin-bottom: 0;">Transform your Figma designs into production-ready React Native components with AI-powered precision</p>
    <p style="color: #6c757d; font-size: 0.9em; margin-top: 0.5rem;">Powered by Google Gemini AI -  Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
