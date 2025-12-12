import time
import os
from google import genai

# Configure the Gemini client
client=genai.Client(api_key='AIzaSyC_j2IYqbRgJVs7K-bfcAOFodz1NGhI8Yw')
# Paths (adjust as needed)
INITIAL_REACT_CODE_PATH = r'C:\Solutions\figma user story trial\output_folder\gib_mobile\mobile_version_native_v1.txt'
API_JSON_DOC_DIR = r'C:\Solutions\figma user story trial\split_files_15k_personal_details'
IMAGE_PATH = r'C:\Solutions\figma user story trial\input_folder\gib_mobile\personaldetails.png'
OUTPUT_DIR = r'C:\Solutions\figma user story trial\output_folder_15k_personal_details'

THEME_COLORS_PATH = r'C:\Solutions\figma user story trial\input_folder\gib_mobile\theme_colors_common.txt'

ENRICH_PROMPT_TEMPLATE = '''

You are enhancing React Native code with precise design specifications from Figma API JSON data.

---

## CONTEXT

This is **iteration {iteration_number}** of code enrichment. You are refining previously generated code using Figma design data.

**Input Files:**
1. **Current Code** - React Native code from previous iteration (or Step-1 if first iteration)
2. **Theme Colors File** - Pre-defined theme color mappings (key-value pairs)
3. **Figma Design Image** - Visual reference for the screen
4. **Figma API JSON Data** (Part {part_number} of {total_parts}) - Design specifications extracted from Figma

---

## FILE STRUCTURE REMINDER

**Your code must follow this structure (from Step-1):**

```
app/features/{feature}/
├── views/
│   └── {screen-name}/
│       ├── index.tsx          # Main view component (UI only)
│       ├── styles.ts          # StyleSheet definitions
│       ├── types.ts           # TypeScript interfaces/types
│       └── translations.ts    # Translation keys (en/ar)
├── hooks/
│   └── use-{screen-name}.ts   # Custom hook (business logic) - FEATURE LEVEL
└── schemas/
    └── {screen-name}-schema.ts # Yup validation schema - FEATURE LEVEL
```

**Import paths in view component:**
```typescript
// Feature-level imports (TWO LEVELS UP from view)
import {useScreenName} from '../../hooks/use-screen-name';
import {ScreenNameSchema} from '../../schemas/screen-name-schema';

// Local view imports
import {getStyles} from './styles';
import {ScreenNameProps} from './types';
```

---

## CRITICAL INSTRUCTIONS

### ❌ DO NOT:
- Change existing component structure or component types
- Remove or replace custom component imports
- Create new components or mock implementations
- **Change file paths or file structure (hooks/schemas stay at feature level)**
- **Move hooks or schemas into view folder**
- Alter business logic or state management in hooks
- Modify validation schemas or form logic
- Modify TypeScript types unless adding design-specific ones
- Use hardcoded color hex values
- Change import paths for hooks/schemas

### ✅ DO:
- Enrich styles with precise values from Figma API JSON
- Map Figma colors to existing theme color keys carefully
- Update padding, margin, spacing, borderRadius from Figma data
- Apply font families, font sizes, font weights from Figma
- Add shadows, borders, opacity values from Figma
- Maintain existing component usage and imports
- **Keep hooks at feature level:** `app/features/{feature}/hooks/`
- **Keep schemas at feature level:** `app/features/{feature}/schemas/`
- Keep file structure: views/{screen}/index.tsx, styles.ts, types.ts, translations.ts
- Use `theme.colors['theme-key']` for all colors
- Preserve import paths (../../hooks/, ../../schemas/)

---

## THEME COLOR MAPPING

**Available Theme Colors (from theme_colors_common.txt):**

{theme_colors_content}

**Color Mapping Rules:**
1. **Extract color from Figma JSON** - Look for color values in RGB, RGBA, or hex format
2. **Find closest theme match** - Match Figma color to the closest existing theme key
3. **Use theme key in code** - Replace with `theme.colors['theme-key-name']`
4. **Priority mapping:**
   - Background colors → `background-01` to `background-04`
   - Surface colors → `surface-*` variations
   - Text colors → `content-primary`, `content-secondary`, `content-tertiary`
   - Interactive elements → `surface-interactive-*` or `content-interactive-*`
   - Borders → `border-*` variations
   - Icons → `icon-*` variations

**Example Mapping:**

```
Figma: {"r": 0.098, "g": 0.027, "b": 0.290, "a": 1} → #19074A → primary-100
Code: backgroundColor: theme.colors['background-04'] // maps to primary-100

Figma: {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1} → #FFFFFF → neutral-00
Code: color: theme.colors['content-inverted-primary'] // white text
```

---

## FIGMA API JSON ANALYSIS

**From the provided Figma JSON data, extract and apply:**

### 1. **Layout & Spacing**
- `paddingLeft`, `paddingRight`, `paddingTop`, `paddingBottom`
- `itemSpacing` (gap between flex children)
- `layoutMode` (HORIZONTAL, VERTICAL)
- `primaryAxisAlignItems` (flex alignment)
- `counterAxisAlignItems` (cross-axis alignment)
- `layoutGrow` (flex grow)
- `layoutAlign` (stretch, center, etc.)

### 2. **Typography**
- `fontFamily` (map to closest available system font or custom font)
- `fontSize`
- `fontWeight` (100-900)
- `lineHeightPx` or `lineHeightPercent`
- `letterSpacing`
- `textAlignHorizontal` (LEFT, CENTER, RIGHT)
- `textAlignVertical` (TOP, CENTER, BOTTOM)
- `textCase` (UPPER, LOWER, TITLE)

### 3. **Colors**
- `fills` array (background colors, gradient fills)
- `strokes` array (border colors)
- `color` (text color)
- Map ALL colors to theme keys - NEVER use raw hex/RGB values

### 4. **Visual Effects**
- `cornerRadius` or `rectangleCornerRadii` (border radius)
- `effects` array (shadows, blurs)
  - `type`: DROP_SHADOW, INNER_SHADOW, LAYER_BLUR
  - `color`, `offset`, `radius`, `spread`
- `opacity`
- `strokeWeight` (border width)

### 5. **Constraints & Sizing**
- `constraints` (min/max width, height)
- `minWidth`, `maxWidth`, `minHeight`, `maxHeight`
- `layoutSizingHorizontal`, `layoutSizingVertical` (FIXED, HUG, FILL)

---

## ENRICHMENT PROCESS

### Step 1: Identify Components in Figma JSON
- Match Figma layer names to React Native components in view
- Find corresponding nodes in JSON by `name`, `id`, or `type`
- Note which file each enrichment applies to (view, styles, hooks, schemas)

### Step 2: Extract Design Properties
- For each matched component, extract all relevant properties
- Note down values for spacing, colors, typography, effects
- **Focus on styles.ts enrichment** - business logic stays in hooks

### Step 3: Map Colors to Theme
- Convert Figma color values to theme keys
- Document mapping decisions inline with comments
- Example: `// Figma: #19074A → primary-100 → background-04`

### Step 4: Update Styles
- Apply extracted values to StyleSheet in `styles.ts`
- Update `getStyles()` function with precise measurements
- Add responsive considerations if needed
- **Do not modify hooks or schemas** unless Figma reveals new validation requirements

### Step 5: Validate File Structure
- Ensure hooks remain at: `app/features/{feature}/hooks/use-{screen-name}.ts`
- Ensure schemas remain at: `app/features/{feature}/schemas/{screen-name}-schema.ts`
- Verify import paths are correct (../../hooks/, ../../schemas/)
- Check all files maintain their separation of concerns

---

## OUTPUT FORMAT

Provide the enriched code maintaining the EXACT file structure from Step-1:

```
###FilePath: app/features/{feature}/views/{screen-name}/index.tsx
[Component implementation - keep existing structure, imports, logic]
[Import hooks from: ../../hooks/use-{screen-name}]
[Import schemas from: ../../schemas/{screen-name}-schema]

###FilePath: app/features/{feature}/hooks/use-{screen-name}.ts
[Custom hook - typically unchanged unless new business logic needed]
[Keep at FEATURE LEVEL, not in view folder]

###FilePath: app/features/{feature}/schemas/{screen-name}-schema.ts
[Validation schema - typically unchanged unless new validation rules needed]
[Keep at FEATURE LEVEL, not in view folder]

###FilePath: app/features/{feature}/views/{screen-name}/styles.ts
[ENRICHED styles with Figma values and theme color mappings]
[Most enrichment happens here]

###FilePath: app/features/{feature}/views/{screen-name}/types.ts
[Types/interfaces - add any design-specific types if needed]

###FilePath: app/features/{feature}/views/{screen-name}/translations.ts
[Translation keys - typically unchanged unless new text discovered in Figma]
```

---

## ENRICHMENT CHECKLIST

For each component/element, verify:
- [ ] Background color mapped to theme key (from Figma `fills`)
- [ ] Text color mapped to theme key (from Figma `color`)
- [ ] Border color mapped to theme key (from Figma `strokes`)
- [ ] Padding values applied (from Figma `padding*`)
- [ ] Margin/spacing applied (from Figma `itemSpacing`)
- [ ] Font family applied (from Figma `fontFamily`)
- [ ] Font size applied (from Figma `fontSize`)
- [ ] Font weight applied (from Figma `fontWeight`)
- [ ] Line height applied (from Figma `lineHeight*`)
- [ ] Border radius applied (from Figma `cornerRadius`)
- [ ] Shadows applied (from Figma `effects`)
- [ ] Opacity applied if < 1 (from Figma `opacity`)
- [ ] Alignment/justification applied (from Figma layout properties)
- [ ] **Hooks remain at feature level** (not moved into view)
- [ ] **Schemas remain at feature level** (not moved into view)
- [ ] **Import paths preserved** (../../hooks/, ../../schemas/)

---

## EXAMPLE ENRICHMENT

**Before (Step-1 Code in styles.ts):**

```typescript
title: {
  fontSize: 24,
  fontWeight: 'bold',
  color: theme.colors['content-primary'],
  marginBottom: 16,
},
```

**After (Enriched with Figma JSON):**

```typescript
title: {
  fontSize: 28, // from Figma: fontSize
  fontWeight: '700', // from Figma: fontWeight
  lineHeight: 36, // from Figma: lineHeightPx
  letterSpacing: -0.5, // from Figma: letterSpacing
  color: theme.colors['content-inverted-primary'], // Figma fill: #FFFFFF → neutral-00 → content-inverted-primary
  marginBottom: 12, // from Figma: itemSpacing
  paddingHorizontal: 24, // from Figma: paddingLeft + paddingRight
},
```

**File Structure Example:**

```typescript
###FilePath: app/features/credit-card/views/monthly-expenses/index.tsx

// Feature-level imports (correct path - TWO LEVELS UP)
import {useMonthlyExpenses} from '../../hooks/use-monthly-expenses';
import {MonthlyExpensesSchema} from '../../schemas/monthly-expenses-schema';

// Local imports
import {getStyles} from './styles';
import {MonthlyExpensesProps} from './types';

// Component remains unchanged from Step-1
const MonthlyExpenses: React.FC<MonthlyExpensesProps> = ({navigation}) => {
  // ... existing code
};

###FilePath: app/features/credit-card/hooks/use-monthly-expenses.ts
[Typically unchanged - business logic stays the same]

###FilePath: app/features/credit-card/schemas/monthly-expenses-schema.ts
[Typically unchanged - validation rules stay the same]

###FilePath: app/features/credit-card/views/monthly-expenses/styles.ts
[ENRICHED with Figma values - main focus of enrichment]
```

---

## SPECIAL NOTES FOR ITERATIVE ENRICHMENT

**Iteration {iteration_number} Focus:**
- This is part {part_number} of {total_parts} of Figma JSON data
- Focus on enriching components/sections covered in this JSON chunk
- Preserve all enrichments from previous iterations
- Build upon (don't overwrite) previously refined styles
- If a property was already enriched in a previous iteration, keep it unless this iteration provides more specific data
- **Always maintain file structure** - hooks and schemas at feature level

**Handling Conflicts:**
- If current Figma data conflicts with previous iteration, use the MORE SPECIFIC value
- Document any conflicts in inline comments
- Prioritize visual accuracy to the Figma design image
- **Never change file locations or import paths**

**File Structure Validation:**
- After enrichment, verify:
  - ✅ Hooks are at: `app/features/{feature}/hooks/`
  - ✅ Schemas are at: `app/features/{feature}/schemas/`
  - ✅ View files are at: `app/features/{feature}/views/{screen-name}/`
  - ✅ Import paths use `../../hooks/` and `../../schemas/`
  - ✅ No business logic leaked into view component

---

## WHAT TYPICALLY GETS ENRICHED

**High Frequency (Almost Every Iteration):**
- `styles.ts` - Colors, spacing, typography, shadows, borders
- `index.tsx` - Style prop values, inline style adjustments

**Medium Frequency (Sometimes):**
- `types.ts` - New style prop interfaces if Figma reveals complex patterns
- `translations.ts` - New text if Figma has content not in Step-1 code

**Low Frequency (Rarely):**
- `hooks/use-{screen-name}.ts` - Only if Figma reveals new business rules
- `schemas/{screen-name}-schema.ts` - Only if Figma reveals new validation requirements

**Focus 90% of enrichment on `styles.ts`** - that's where design precision matters most.

---

## INPUTS

**Current Code (from previous iteration):**
{current_code}

**Figma API JSON Data (Part {part_number}):**
{figma_json_chunk}

**Figma Design Image Reference:**
[Attached]

---

## TASK

Enrich the current code with design specifications from the provided Figma JSON chunk. 

**Key Requirements:**
1. ✅ Maintain file structure (hooks/schemas at feature level)
2. ✅ Preserve import paths (../../hooks/, ../../schemas/)
3. ✅ Focus enrichment on styles.ts
4. ✅ Map all colors to theme keys
5. ✅ Apply precise Figma measurements
6. ✅ Keep business logic in hooks unchanged (unless absolutely necessary)
7. ✅ Keep validation in schemas unchanged (unless new rules found)
8. ✅ Document color mappings with inline comments

Output the complete enriched code ready for the next iteration or final integration, with proper file structure and import paths maintained.

'''

def load_file_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

def load_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            return f.read()
    else:
        raise FileNotFoundError(f"Image not found: {image_path}")

def get_text_files_in_directory(directory):
    """Return a list of .txt files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.txt') and os.path.isfile(os.path.join(directory, f))]

def call_gemini(react_code, api_json_doc, image_data, theme_file_content):
    """Call Gemini API using client.models.generate_content structure."""
    
    final_prompt = ENRICH_PROMPT_TEMPLATE.replace('{theme_colors_content}', theme_file_content)
    final_prompt = final_prompt.replace('{current_code}', react_code)
    final_prompt = final_prompt.replace('{figma_json_chunk}', api_json_doc)


    # client = genai.GenerativeAI()
    print(final_prompt)
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            genai.types.Part.from_bytes(
                data=image_data,
                mime_type='image/png',
            ),
            final_prompt
        ]
    )

    return response.text

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load initial React code and image
    react_code = load_file_content(INITIAL_REACT_CODE_PATH)
    image_data = load_image(IMAGE_PATH)
    theme_file_content = load_file_content(THEME_COLORS_PATH)
    
    # Get list of text files in the API_JSON_DOC_DIR
    text_files = get_text_files_in_directory(API_JSON_DOC_DIR)
    if not text_files:
        raise FileNotFoundError(f"No .txt files found in {API_JSON_DOC_DIR}")
    
    print(f"Found {len(text_files)} text files in {API_JSON_DOC_DIR}. Will perform {len(text_files)} LLM calls.")
    
    current_react_code = react_code
    for i, text_file in enumerate(text_files, 1):
        # Load text data
        text_file_path = os.path.join(API_JSON_DOC_DIR, text_file)
        api_json_doc = load_file_content(text_file_path)
        
        # Perform LLM call with image
        print(f"Starting LLM call {i} with file {text_file}...")
        start_time = time.time()
        enriched_code = call_gemini(current_react_code, api_json_doc, image_data, theme_file_content)
        print(f"LLM call {i} completed in {time.time() - start_time:.2f} seconds")
        
        # Save the enriched output
        output_file = os.path.join(OUTPUT_DIR, f'enriched_react_code_{i}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(enriched_code)
        print(f"Saved enriched code to {output_file}")
        
        # Use the output as input for the next iteration
        current_react_code = enriched_code
        
        # Wait 5 seconds before the next call (except for the last file)
        if i < len(text_files):
            print("Waiting 5 seconds before next LLM call...")
            time.sleep(60)
    
    print(f"Completed {len(text_files)} LLM calls. All enriched code files saved in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()