GENERATE_PROMPT = '''

Generate React Native screen code from the attached design image for integration into an existing project.

**Project Configuration:**
- React: 19.1.1
- React Native: 0.82.1
- Gradle: 9.0.0
- TypeScript: Required

---

## CRITICAL INSTRUCTIONS

**DO NOT:**
- Create mock components or mock functions
- Recreate any existing components
- Generate placeholder/TODO comments
- Create standalone App.tsx files
- Use `import * as Components` syntax
- Use `<Components.Label>` or any namespace-based component usage
- Use relative imports for hooks, schemas, or shared components when a path alias exists
- Introduce circular dependencies between files or modules
- Use ScaledSheet or react-native-size-matters library
- Use string-based spacing syntax (e.g., '20@vs', '16@s')
- Use styled-components or any CSS-in-JS libraries
- Use hardcoded color hex values
- Use inline styles for complex styling

**DO:**
- Use existing custom components with proper import statements
- Use direct component imports: `import {Label, Input} from '@app/components'`
- Use path aliases (@app, @features, @hooks, @components) for all non-local imports
- Use direct component syntax: `<Label>` instead of `<Components.Label>`
- Follow the existing project structure and patterns
- Generate production-ready, integration-ready code
- Use proper file path format: `###FilePath: app/features/{feature}/views/{screen-name}/index.tsx`
- Separate business logic into custom hooks
- Define validation schemas using Yup
- Use Formik for form management
- Match the Figma design structure, layout, spacing, and alignment as closely as possible
- Ensure all styles are correctly typed for React Native (ViewStyle, TextStyle, ImageStyle, etc.)
- Use standard React Native StyleSheet.create() only
- Use number literals for all spacing (paddingTop: 20, not '20@vs')
- Keep styles in separate styles.ts file
- Use typed StyleSheet interface (interface Styles {...})
- Import StyleSheet from 'react-native', not third-party packages
---

## FILE STRUCTURE & ARCHITECTURE

**IMPORTANT:** Hooks and Schemas are at the **feature level**, NOT inside the view folder.

app/features/{feature}/
├── views/
│ └── {screen-name}/
│ ├── index.tsx # Main view component (UI only)
│ ├── styles.ts # StyleSheet definitions
│ ├── types.ts # TypeScript interfaces/types
│ └── translations.ts # Translation keys (en/ar)
├── hooks/
│ └── use-{screen-name}.ts # Custom hook (business logic, state, handlers)
└── schemas/
└── {screen-name}-schema.ts # Yup validation schema & initial values


**Example Structure:**

app/features/credit-card/
├── views/
│ ├── monthly-expenses/
│ │ ├── index.tsx
│ │ ├── styles.ts
│ │ ├── types.ts
│ │ └── translations.ts
│ └── personal-details/
│ ├── index.tsx
│ ├── styles.ts
│ ├── types.ts
│ └── translations.ts
├── hooks/
│ ├── use-monthly-expenses.ts
│ └── use-personal-details.ts
└── schemas/
├── monthly-expenses-schema.ts
└── personal-details-schema.ts


### Architecture Principles:

1. **View (views/{screen-name}/index.tsx):** Pure UI component, no business logic
2. **Hook (hooks/use-{screen-name}.ts):** All state, logic, handlers, validation
3. **Schema (schemas/{screen-name}-schema.ts):** Yup validation rules, initial values, types
4. **Styles (views/{screen-name}/styles.ts):** Theme-based StyleSheet with proper TypeScript typing
5. **Types (views/{screen-name}/types.ts):** Component props, navigation types, and any additional interfaces
6. **Translations (views/{screen-name}/translations.ts):** i18n keys and values

---

## PATH ALIASES & TSCONFIG

The project uses the following TypeScript configuration for path aliases:

{
"baseUrl": ".",
"paths": {
"": ["./"],
"@app/": ["app/"],
"@features/": ["app/features/"],
"@hooks/": ["app/hooks/"],
"@components/": ["app/components/"]
}
}


**Import Priority Rules:**

1. ✅ Use `@features/{feature}/hooks/use-screen-name` for hooks
2. ✅ Use `@features/{feature}/schemas/screen-name-schema` for schemas
3. ✅ Use `@app/components` for shared UI components
4. ✅ Use `@app/assets/svg` for icons and SVGs
5. ✅ Use `@app/constants` for constants and enums
6. ❌ Avoid `../../hooks/use-screen-name` when a path alias is available
7. ❌ Avoid `import * as Components from '@app/components'`
8. ✅ Only use relative imports for local view-level files like `./styles`, `./types`, `./translations`

---

## NAMING CONVENTIONS & STANDARDS

{conventions_and_standards}

(Above content includes: strict import order, component ID naming, translation key patterns, hook & schema patterns, and TypeScript style guidelines.)

---

## TYPESCRIPT & STYLE PROP REQUIREMENTS

**Goal:** Ensure correct typing of all styles and style props for React Native components.

### General Rules

- Do **not** define a `StyleProps` interface in `types.ts` that wraps styles in `StyleProp<T>`.
- Define raw styles (ViewStyle, TextStyle, ImageStyle) in `styles.ts` and type `StyleSheet.create` with a `Styles` interface.
- Component props that accept styles (like `Label.style`) should be typed as `StyleProp<TextStyle>` etc. in the component definition (already done in existing components).
- Passing `styles.someTextStyle` (type `TextStyle`) into a prop of type `StyleProp<TextStyle>` is valid and expected.

### In types.ts

import {NativeStackNavigationProp} from '@react-navigation/native-stack';

export interface ScreenNameProps {
navigation: NativeStackNavigationProp<any>;
// Add other non-style props if needed
}

### In styles.ts

import {StyleSheet, ViewStyle, TextStyle} from 'react-native';
import {Theme} from 'react-core';

interface Styles {
container: ViewStyle;
headerContainer: ViewStyle;
datesContainer: ViewStyle;
dateItem: ViewStyle;
sectionTitle: TextStyle;
dateLabel: TextStyle;
// Add other styles as needed
}

export const getStyles = ({theme}: {theme: Theme}): Styles => {
return StyleSheet.create<Styles>({
container: {
flex: 1,
paddingHorizontal: 20,
},
headerContainer: {
marginBottom: 16,
},
datesContainer: {
flexDirection: 'row',
justifyContent: 'space-between',
},
dateItem: {
flex: 1,
alignItems: 'center',
},
sectionTitle: {
fontSize: 16,
fontWeight: '600',
color: theme.colors.text.primary,
},
dateLabel: {
fontSize: 14,
color: theme.colors.text.secondary,
},
});
};


**Example usage in View:**

<Label
id="LabelInstallmentFrom"
text={t('MeemAshalInstallmentsLblFrom')}
variant={variants.bodyRegularS}
style={styles.dateLabel} // Label.style is StyleProp<TextStyle>
/>


---

## DESIGN MATCHING REQUIREMENTS

**CRITICAL: Match the Figma design structure, layout, spacing, and alignment as closely as possible.**

When analyzing the attached Figma design image:

1. **Layout Structure:** Replicate the exact component hierarchy (containers, sections, cards, rows, etc.).
2. **Spacing:** Match margins, paddings, gaps, and spacing between elements.
3. **Alignment:** Preserve all horizontal and vertical alignments.
4. **Typography:** Respect font size, weight, color, and line-height.
5. **Colors:** Use theme colors that correspond to the design palette.
6. **Sizing:** Match widths, heights, and flex settings where visible.
7. **Visual Hierarchy:** Maintain the same grouping and emphasis as the design.

**Layout Checklist:**

- [ ] Main container type identified (e.g., ScreenContainer, ScrollView, etc.)
- [ ] Header and title areas structured correctly
- [ ] Form sections grouped as in design
- [ ] Buttons placed correctly (bottom fixed, inline, etc.)
- [ ] Any decorative or informational components (cards, tags, chips) mapped to existing components
- [ ] Icons and images placed and sized as in Figma

---

## 1. COMPONENT MAPPING

{component_mapping}

---

## 2. EXISTING CUSTOM COMPONENTS

{existing_components}

**Usage Instructions:**
- Review all provided component definitions (props, types, usage patterns).
- Match each Figma element to the closest existing component by purpose and behavior.
- Use these components instead of creating new ones.
- Import components directly: `import {ScreenContainer, Label, Input, SubmitButton} from '@app/components'`.
- Use direct JSX usage, e.g., `<Label />` rather than `<Components.Label />`.
- Follow the exact prop structures and conventions from the provided components.

---

## 3. SAMPLE WORKING CODE PATTERNS

{sample_code}

**Follow these patterns for:**
- File structure (hooks and schemas at feature level)
- Import statement organization (strict order with path aliases)
- Direct component imports (no namespace imports)
- Hook implementation pattern
- Schema validation pattern
- Component composition and layout
- State management via custom hooks
- Theme usage with `useNewTheme()`
- Translation with `translation.useTranslation()`
- Navigation patterns

---

## 4. PROJECT STRUCTURE

{package_structure}

**Generate code following this structure:**
- `app/features/{feature-name}/views/{screen-name}/index.tsx`
- `app/features/{feature-name}/views/{screen-name}/styles.ts`
- `app/features/{feature-name}/views/{screen-name}/types.ts`
- `app/features/{feature-name}/views/{screen-name}/translations.ts`
- `app/features/{feature-name}/hooks/use-{screen-name}.ts` ← **Feature level**
- `app/features/{feature-name}/schemas/{screen-name}-schema.ts` ← **Feature level**

---

## 5. USER STORIES & BUSINESS LOGIC

{user_stories_file_content}

**Implement according to:**
- Field validation rules (define in schemas)
- Mandatory vs optional fields (Yup validation)
- Conditional field visibility (logic in hooks)
- Data flow and state management (centralized in hooks)
- Form submission and navigation (handlers in hooks)

---

## GENERATION REQUIREMENTS

### Design Analysis

1. Analyze the attached Figma design image carefully.
2. Match structure, layout, spacing, and alignment as closely as possible.
3. Identify all UI components, layouts, interactions, text content, and styling.
4. Map each visual element to existing custom components.
5. Extract text content, colors, spacing, and typography.
6. Identify form fields that need validation.
7. Note component hierarchy, nesting, and flex behavior.
8. Respect safe-area, scrolling, and keyboard behavior if indicated.

### Code Structure

Generate files in this format:

###FilePath: app/features/{feature}/views/{screen-name}/index.tsx
[View component - UI only, uses custom hook, direct component imports]

###FilePath: app/features/{feature}/hooks/use-{screen-name}.ts
[Custom hook - all business logic, state, handlers]

###FilePath: app/features/{feature}/schemas/{screen-name}-schema.ts
[Yup schema, initial values, types]

###FilePath: app/features/{feature}/views/{screen-name}/styles.ts
[Styles implementation with typed StyleSheet and Theme]

###FilePath: app/features/{feature}/views/{screen-name}/types.ts
[Types/interfaces for props]

###FilePath: app/features/{feature}/views/{screen-name}/translations.ts
[Translation keys with en and ar objects]


### Implementation Checklist

- [ ] **Strict import order:** React → Third-party → Components → Theme/utilities → Assets → Feature imports (with path aliases) → Local imports
- [ ] **Use path aliases** for hooks, schemas, components, constants, and assets
- [ ] **Direct component imports:** `import {Label, Input} from '@app/components'`
- [ ] **Direct component usage:** `<Label>` not `<Components.Label>`
- [ ] **Hooks at feature level:** `@features/{feature}/hooks/use-{screen-name}`
- [ ] **Schemas at feature level:** `@features/{feature}/schemas/{screen-name}-schema`
- [ ] **View is pure UI** (no business logic, only calls the custom hook)
- [ ] **All state and handlers in custom hook** (useState, useMemo, callbacks, navigation)
- [ ] **Formik** is used inside the hook for form state and validation
- [ ] **Yup** schemas define all validation rules
- [ ] **Translations.ts** generated with both `en` and `ar` objects
- [ ] **Component IDs** follow `ComponentNameFieldName` TitleCase pattern
- [ ] **Translation keys** follow `JourneyScreenNameComponentAbbreviationFieldName`
- [ ] **Styles** are typed using `ViewStyle`, `TextStyle`, `ImageStyle` in `styles.ts`
- [ ] **No circular dependencies** between views, hooks, schemas, and components
- [ ] **Figma layout** is matched for structure, spacing, and alignment

---

## OUTPUT FORMAT

Provide complete, production-ready code organized by file path:

1. **View component** (views/{screen-name}/index.tsx) – Pure UI using custom hook, direct imports.
2. **Custom hook** (hooks/use-{screen-name}.ts) – All business logic at feature level.
3. **Schema** (schemas/{screen-name}-schema.ts) – Yup validation at feature level.
4. **Styles** (views/{screen-name}/styles.ts) – Theme-based StyleSheet with typed interfaces.
5. **Types** (views/{screen-name}/types.ts) – TypeScript interfaces for props.
6. **Translations** (views/{screen-name}/translations.ts) – i18n keys and values.

**File Path Examples:**
###FilePath: app/features/credit-card/views/monthly-expenses/index.tsx
###FilePath: app/features/credit-card/hooks/use-monthly-expenses.ts
###FilePath: app/features/credit-card/schemas/monthly-expenses-schema.ts
###FilePath: app/features/credit-card/views/monthly-expenses/styles.ts
###FilePath: app/features/credit-card/views/monthly-expenses/types.ts
###FilePath: app/features/credit-card/views/monthly-expenses/translations.ts

**Code must be:**
- Ready to integrate into the existing project
- Free of mocks, placeholders, or TODOs
- Following exact patterns from the provided samples
- Using only provided custom components with direct imports
- Properly separated (UI vs logic)
- Using custom hooks for all business logic at feature level
- Using Yup schemas for all validation at feature level
- Properly typed with TypeScript, including style types in `styles.ts`
- Following all naming conventions and path alias rules
- Using translation keys for all text
- Matching the Figma design structure, layout, spacing, and alignment as closely as possible
- Free from circular dependencies

Generate the code now based on the attached design image, following ALL conventions and patterns above.

'''

ENRICH_PROMPT = '''

You are enhancing React Native code with precise design specifications from Figma API JSON data.

---

## CONTEXT

This is **iteration {iteration_number}** of code enrichment. You are refining previously generated code using Figma design data.

**Input Files:**
1. **Current Code** - React Native code from previous iteration (or Step-1 if first iteration)
2. **Theme Colors & Typography File** - Pre-defined theme color mappings and font/typography system
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

**Import paths in view component (using PATH ALIASES):**
```typescript
// Feature-level imports using PATH ALIASES
import {useScreenName} from '@features/{feature}/hooks/use-screen-name';
import {ScreenNameSchema} from '@features/{feature}/schemas/screen-name-schema';

// Component imports using direct imports
import {
  ScreenContainer,
  Label,
  Input,
  SubmitButton,
} from '@app/components';

// Theme and utilities
import {useNewTheme, Theme, translation} from 'react-core';

// Local view imports (relative paths)
import {getStyles} from './styles';
import {ScreenNameProps} from './types';
import {variants} from '@app/components/label/types';
```

---

## CRITICAL INSTRUCTIONS

### ❌ DO NOT:
- Change existing component structure or component types
- Remove or replace custom component imports
- Create new components or mock implementations
- Use `import * as Components` syntax
- Use `<Components.Label>` component syntax
- **Change file paths or file structure (hooks/schemas stay at feature level)**
- **Move hooks or schemas into view folder**
- Alter business logic or state management in hooks
- Modify validation schemas or form logic
- Modify TypeScript types unless adding design-specific ones
- Use hardcoded color hex values
- Use hardcoded font families (use theme typography system)
- Change import paths - use path aliases

### ✅ DO:
- Use direct component imports: `import {Label, Input} from '@app/components'`
- Use direct component syntax: `<Label>` not `<Components.Label>`
- Use path aliases: `@features/{feature}/hooks/`, `@app/components`
- Enrich styles with precise values from Figma API JSON
- Map Figma colors to existing theme color keys carefully
- Map Figma typography to theme typography variants (TitleXL, BodyRegularM, etc.)
- Update padding, margin, spacing, borderRadius from Figma data
- Apply font properties via `variants` prop on components (Label, Text)
- Add shadows, borders, opacity values from Figma
- Maintain existing component usage and imports
- **Keep hooks at feature level:** `app/features/{feature}/hooks/`
- **Keep schemas at feature level:** `app/features/{feature}/schemas/`
- Keep file structure: views/{screen}/index.tsx, styles.ts, types.ts, translations.ts
- Use `theme.colors['theme-key']` for all colors
- Use theme typography system for fonts
- Preserve proper import patterns (path aliases, direct imports)

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

**Example Color Mapping:**

```typescript
// Figma: {"r": 0.098, "g": 0.027, "b": 0.290, "a": 1} → #19074A → primary-100
backgroundColor: theme.colors['background-04'], // maps to primary-100

// Figma: {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1} → #FFFFFF → neutral-00
color: theme.colors['content-inverted-primary'], // white text
```

---

## THEME TYPOGRAPHY SYSTEM

**Available Typography Variants:**

The project uses a predefined typography system. Components like `Label` accept a `variant` prop.

**Typography Variants (from theme_colors_common.txt):**

```typescript
// Title variants
TitleXL: { fontFamily: 'figtree', fontSize: 28, fontWeight: '600', lineHeight: 32 }
TitleL:  { fontFamily: 'figtree', fontSize: 24, fontWeight: '800', lineHeight: 28 }
TitleM:  { fontFamily: 'figtree', fontSize: 20, fontWeight: '800', lineHeight: 28 }
TitleS:  { fontFamily: 'figtree', fontSize: 18, fontWeight: '600', lineHeight: 24 }
TitleXS: { fontFamily: 'figtree', fontSize: 16, fontWeight: '800', lineHeight: 24 }

// Body Semibold variants
BodySemiboldL:  { fontFamily: 'figtree', fontSize: 18, fontWeight: '800', lineHeight: 24 }
BodySemiboldS:  { fontFamily: 'figtree', fontSize: 14, fontWeight: '800', lineHeight: 20 }
BodySemiboldXS: { fontFamily: 'figtree', fontSize: 12, fontWeight: '800', lineHeight: 16 }

// Body Medium variants
BodyMediumL:  { fontFamily: 'figtree', fontSize: 18, fontWeight: '600', lineHeight: 24 }
BodyMediumM:  { fontFamily: 'figtree', fontSize: 16, fontWeight: '600', lineHeight: 24 }
BodyMediumS:  { fontFamily: 'figtree', fontSize: 14, fontWeight: '600', lineHeight: 20 }
BodyMediumXS: { fontFamily: 'figtree', fontSize: 12, fontWeight: '600', lineHeight: 16 }

// Body Regular variants
BodyRegularL:  { fontFamily: 'figtree', fontSize: 18, fontWeight: '400', lineHeight: 24 }
BodyRegularM:  { fontFamily: 'figtree', fontSize: 16, fontWeight: '400', lineHeight: 24 }
BodyRegularS:  { fontFamily: 'figtree', fontSize: 14, fontWeight: '400', lineHeight: 20 }
BodyRegularXS: { fontFamily: 'figtree', fontSize: 12, fontWeight: '400', lineHeight: 16 }
```

**Typography Mapping Rules:**

1. **Extract from Figma JSON:**
   - `fontSize` (in pixels)
   - `fontWeight` (100-900)
   - `lineHeightPx` or `lineHeightPercent`
   - `fontFamily` (usually "Figtree" or similar)

2. **Map to closest variant:**
   - Match fontSize first (12, 14, 16, 18, 20, 24, 28)
   - Then match fontWeight (400=Regular, 600=Medium, 800=Semibold)
   - Choose Title vs Body based on context (headings = Title, content = Body)

3. **Apply via component props:**
   - Use `variant` prop on Label/Text components
   - Import from: `import {variants} from '@app/components/label/types'`
   - Example: `<Label variant={variants.titleL} />`

4. **Override when needed:**
   - If exact Figma value doesn't match any variant, add style override
   - Example: `<Label variant={variants.bodyRegularM} style={{fontSize: 15}} />`

**Typography Application Examples:**

```typescript
// Method 1: Use variant prop (PREFERRED)
<Label
  id="LabelTitle"
  text={t('ScreenLblTitle')}
  variant={variants.titleL}  // fontSize: 24, fontWeight: '800'
  style={styles.title}  // Only for color, spacing, etc.
/>

// Method 2: Override variant if Figma doesn't match exactly
<Label
  id="LabelSubtitle"
  text={t('ScreenLblSubtitle')}
  variant={variants.bodyRegularM}
  style={{
    ...styles.subtitle,
    fontSize: 15,  // Figma uses 15px, override variant's 16px
  }}
/>

// Method 3: In styles.ts (for non-Label components)
const styles = StyleSheet.create({
  customText: {
    fontFamily: 'figtree',
    fontSize: 16,
    fontWeight: '400',
    lineHeight: 24,
    color: theme.colors['content-primary'],
  },
});
```

**Typography Checklist:**
- [ ] Extract fontSize, fontWeight, lineHeight from Figma JSON
- [ ] Map to closest typography variant
- [ ] Apply via `variant` prop on Label/Text components
- [ ] Use style override only when necessary for non-standard values
- [ ] Never hardcode font families - use 'figtree' from theme
- [ ] Document any custom typography in comments

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
- `fontFamily` → Map to 'figtree' (project standard)
- `fontSize` → Map to variant or use exact value
- `fontWeight` → Map to variant (400, 600, 800)
- `lineHeightPx` or `lineHeightPercent` → Map to variant or use exact
- `letterSpacing` → Apply if specified
- `textAlignHorizontal` → LEFT, CENTER, RIGHT
- `textAlignVertical` → TOP, CENTER, BOTTOM
- `textCase` → UPPER, LOWER, TITLE

**Typography Application Priority:**
1. Try to match a variant (TitleXL, BodyRegularM, etc.)
2. If no exact match, choose closest variant + style override
3. Document the mapping: `// Figma: 24px/800 → variants.titleL`

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
- **Map typography to variants first** before considering overrides
- **Focus on styles.ts enrichment** - business logic stays in hooks

### Step 3: Map Colors & Typography to Theme
- Convert Figma color values to theme keys
- Map Figma typography to typography variants
- Document mapping decisions inline with comments
- Example: `// Figma: #19074A → primary-100 → background-04`
- Example: `// Figma: 24px/800 → variants.titleL`

### Step 4: Update Styles & Components
- Apply extracted values to StyleSheet in `styles.ts`
- Update component `variant` props in `index.tsx` for typography
- Add style overrides only when variant doesn't match exactly
- Update `getStyles()` function with precise measurements
- Add responsive considerations if needed
- **Do not modify hooks or schemas** unless Figma reveals new validation requirements

### Step 5: Validate File Structure & Imports
- Ensure hooks remain at: `app/features/{feature}/hooks/use-{screen-name}.ts`
- Ensure schemas remain at: `app/features/{feature}/schemas/{screen-name}-schema.ts`
- Verify import paths use path aliases: `@features/{feature}/hooks/`
- Verify direct component imports: `import {Label} from '@app/components'`
- Check all files maintain their separation of concerns
- Verify no `import * as Components` usage

---

## OUTPUT FORMAT

Provide the enriched code maintaining the EXACT file structure from Step-1 with proper import patterns:

```
###FilePath: app/features/{feature}/views/{screen-name}/index.tsx
[Component implementation - keep existing structure]
[Use direct imports: import {Label, Input} from '@app/components']
[Use path aliases: import {useScreenName} from '@features/{feature}/hooks/use-screen-name']
[Apply typography via variant props on Label components]

###FilePath: app/features/{feature}/hooks/use-{screen-name}.ts
[Custom hook - typically unchanged unless new business logic needed]
[Keep at FEATURE LEVEL, not in view folder]

###FilePath: app/features/{feature}/schemas/{screen-name}-schema.ts
[Validation schema - typically unchanged unless new validation rules needed]
[Keep at FEATURE LEVEL, not in view folder]

###FilePath: app/features/{feature}/views/{screen-name}/styles.ts
[ENRICHED styles with Figma values, theme color mappings, and typography]
[Most enrichment happens here]
[Document color mappings: // Figma: #hex → theme-key]
[Document typography: // Figma: fontSize/weight → variant]

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
- [ ] Typography mapped to variant (TitleXL, BodyRegularM, etc.)
- [ ] Font size applied via variant or style override
- [ ] Font weight applied via variant or style override
- [ ] Line height applied via variant or style override
- [ ] Padding values applied (from Figma `padding*`)
- [ ] Margin/spacing applied (from Figma `itemSpacing`)
- [ ] Border radius applied (from Figma `cornerRadius`)
- [ ] Shadows applied (from Figma `effects`)
- [ ] Opacity applied if < 1 (from Figma `opacity`)
- [ ] Alignment/justification applied (from Figma layout properties)
- [ ] **Direct component imports used** (no `import * as Components`)
- [ ] **Path aliases used** (@features, @app, not relative paths)
- [ ] **Hooks remain at feature level** (not moved into view)
- [ ] **Schemas remain at feature level** (not moved into view)
- [ ] **Component syntax is direct** (`<Label>` not `<Components.Label>`)

---

## EXAMPLE ENRICHMENT

**Before (Step-1 Code in index.tsx):**

```typescript
import * as Components from '@app/components';

<Components.Label
  id="LabelTitle"
  text={t('ScreenLblTitle')}
  style={styles.title}
/>
```

**After (Enriched with Typography Variant):**

```typescript
import {Label} from '@app/components';
import {variants} from '@app/components/label/types';

<Label
  id="LabelTitle"
  text={t('ScreenLblTitle')}
  variant={variants.titleL}  // Figma: 24px/800 → TitleL
  style={styles.title}
/>
```

**Before (Step-1 Code in styles.ts):**

```typescript
title: {
  fontSize: 24,
  fontWeight: 'bold',
  color: theme.colors['content-primary'],
  marginBottom: 16,
},
```

**After (Enriched with Figma JSON - styles.ts):**

```typescript
title: {
  // Typography handled by variant prop on component
  // Figma: 24px/800/28 → variants.titleL
  color: theme.colors['content-inverted-primary'], // Figma: #FFFFFF → neutral-00
  marginBottom: 12, // Figma: itemSpacing
  paddingHorizontal: 24, // Figma: paddingLeft + paddingRight
  letterSpacing: -0.5, // Figma: letterSpacing (if not in variant)
},
```

**File Structure Example with Path Aliases:**

```typescript
###FilePath: app/features/credit-card/views/monthly-expenses/index.tsx

// 1. React imports
import React from 'react';
import {View} from 'react-native';

// 2. Direct component imports (NO namespace imports)
import {
  ScreenContainer,
  Label,
  Input,
  SubmitButton,
} from '@app/components';

// 3. Theme and utilities
import {useNewTheme, translation} from 'react-core';
import {variants} from '@app/components/label/types';

// 4. Feature-level imports with PATH ALIASES
import {useMonthlyExpenses} from '@features/credit-card/hooks/use-monthly-expenses';
import {MonthlyExpensesSchema} from '@features/credit-card/schemas/monthly-expenses-schema';

// 5. Local imports
import {getStyles} from './styles';
import {MonthlyExpensesProps} from './types';

const MonthlyExpenses: React.FC<MonthlyExpensesProps> = ({navigation}) => {
  const theme = useNewTheme();
  const styles = getStyles({theme});
  const {t} = translation.useTranslation();

  const {
    totalExpenses,
    onChangeTotal,
    handleNext,
  } = useMonthlyExpenses();

  return (
    <ScreenContainer id="ScreenContainerMonthlyExpenses">
      <View style={styles.container}>
        <Label
          id="LabelTitle"
          text={t('CreditCardMonthlyExpensesLblTitle')}
          variant={variants.titleL}  // Figma: 24px/800 → TitleL
          style={styles.title}
        />
        <Label
          id="LabelSubtitle"
          text={t('CreditCardMonthlyExpensesLblSubtitle')}
          variant={variants.bodyRegularM}  // Figma: 16px/400 → BodyRegularM
          style={styles.subtitle}
        />
      </View>
    </ScreenContainer>
  );
};

export default MonthlyExpenses;


###FilePath: app/features/credit-card/hooks/use-monthly-expenses.ts
[Typically unchanged - business logic stays the same]


###FilePath: app/features/credit-card/schemas/monthly-expenses-schema.ts
[Typically unchanged - validation rules stay the same]


###FilePath: app/features/credit-card/views/monthly-expenses/styles.ts

import {StyleSheet, ViewStyle, TextStyle} from 'react-native';
import {Theme} from 'react-core';

interface Styles {
  container: ViewStyle;
  title: TextStyle;
  subtitle: TextStyle;
}

export const getStyles = ({theme}: {theme: Theme}): Styles => {
  return StyleSheet.create<Styles>({
    container: {
      flex: 1,
      paddingHorizontal: 24, // Figma: paddingLeft + paddingRight
      paddingTop: 32, // Figma: paddingTop
      backgroundColor: theme.colors['background-01'], // Figma: #FAFAFA → neutral-05
    },
    title: {
      // Typography via variant={variants.titleL} on component
      // Figma: 24px/800/28 → TitleL variant
      color: theme.colors['content-primary'], // Figma: #1A1A1A → neutral-100
      marginBottom: 12, // Figma: itemSpacing
      letterSpacing: -0.5, // Figma: letterSpacing (custom)
    },
    subtitle: {
      // Typography via variant={variants.bodyRegularM} on component
      // Figma: 16px/400/24 → BodyRegularM variant
      color: theme.colors['content-secondary'], // Figma: #666666 → neutral-60
      marginBottom: 24, // Figma: itemSpacing
    },
  });
};
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
- **Always use path aliases and direct imports**

**Handling Conflicts:**
- If current Figma data conflicts with previous iteration, use the MORE SPECIFIC value
- Document any conflicts in inline comments
- Prioritize visual accuracy to the Figma design image
- **Never change file locations or import paths**
- **Never revert to namespace imports**

**File Structure & Import Validation:**
- After enrichment, verify:
  - ✅ Hooks are at: `app/features/{feature}/hooks/`
  - ✅ Schemas are at: `app/features/{feature}/schemas/`
  - ✅ View files are at: `app/features/{feature}/views/{screen-name}/`
  - ✅ Import paths use path aliases: `@features/{feature}/hooks/`
  - ✅ Components use direct imports: `import {Label} from '@app/components'`
  - ✅ Components use direct syntax: `<Label>` not `<Components.Label>`
  - ✅ Typography uses variant props where possible
  - ✅ No business logic leaked into view component

---

## WHAT TYPICALLY GETS ENRICHED

**High Frequency (Almost Every Iteration):**
- `styles.ts` - Colors, spacing, shadows, borders (NOT direct font properties)
- `index.tsx` - Typography variant props, style prop adjustments

**Medium Frequency (Sometimes):**
- `types.ts` - New style prop interfaces if Figma reveals complex patterns
- `translations.ts` - New text if Figma has content not in Step-1 code

**Low Frequency (Rarely):**
- `hooks/use-{screen-name}.ts` - Only if Figma reveals new business rules
- `schemas/{screen-name}-schema.ts` - Only if Figma reveals new validation requirements

**Typography Enrichment:**
- Apply via `variant` prop on Label/Text components (90% of cases)
- Override in `style` prop only when Figma uses non-standard values (10% of cases)
- Document mapping: `// Figma: 24px/800 → variants.titleL`

**Focus Distribution:**
- 60% enrichment on `styles.ts` (colors, spacing, effects)
- 30% enrichment on `index.tsx` (typography variants)
- 10% enrichment on other files (types, translations)

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
1. ✅ Use direct component imports: `import {Label} from '@app/components'`
2. ✅ Use direct component syntax: `<Label>` not `<Components.Label>`
3. ✅ Use path aliases: `@features/{feature}/hooks/`, `@app/components`
4. ✅ Map Figma typography to variants (TitleXL, BodyRegularM, etc.)
5. ✅ Apply typography via `variant` prop on Label/Text components
6. ✅ Maintain file structure (hooks/schemas at feature level)
7. ✅ Focus enrichment on styles.ts and component variant props
8. ✅ Map all colors to theme keys
9. ✅ Apply precise Figma measurements
10. ✅ Keep business logic in hooks unchanged (unless absolutely necessary)
11. ✅ Keep validation in schemas unchanged (unless new rules found)
12. ✅ Document color mappings and typography mappings with inline comments

Output the complete enriched code ready for the next iteration or final integration, with proper file structure, import paths, direct component usage, and typography variant application.

'''