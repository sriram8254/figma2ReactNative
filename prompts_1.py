# prompts.py
# All your prompts in one clean, organized file

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

**DO:**
- Use existing custom components with proper import statements
- Follow the existing project structure and patterns
- Generate production-ready, integration-ready code
- Use proper file path format: `###FilePath: app/features/{feature}/views/{screen-name}/index.tsx`
- Separate business logic into custom hooks
- Define validation schemas using Yup
- Use Formik for form management

---

## FILE STRUCTURE & ARCHITECTURE

**IMPORTANT:** Hooks and Schemas are at the **feature level**, NOT inside the view folder.

```
app/features/{feature}/
├── views/
│   └── {screen-name}/
│       ├── index.tsx          # Main view component (UI only)
│       ├── styles.ts          # StyleSheet definitions
│       ├── types.ts           # TypeScript interfaces/types
│       └── translations.ts    # Translation keys (en/ar)
├── hooks/
│   └── use-{screen-name}.ts   # Custom hook (business logic, state, handlers)
└── schemas/
    └── {screen-name}-schema.ts # Yup validation schema & initial values
```

**Example Structure:**
```
app/features/credit-card/
├── views/
│   ├── monthly-expenses/
│   │   ├── index.tsx
│   │   ├── styles.ts
│   │   ├── types.ts
│   │   └── translations.ts
│   └── personal-details/
│       ├── index.tsx
│       ├── styles.ts
│       ├── types.ts
│       └── translations.ts
├── hooks/
│   ├── use-monthly-expenses.ts
│   └── use-personal-details.ts
└── schemas/
    ├── monthly-expenses-schema.ts
    └── personal-details-schema.ts
```

### Architecture Principles:

1. **View (views/{screen-name}/index.tsx):** Pure UI component, no business logic
2. **Hook (hooks/use-{screen-name}.ts):** All state, logic, handlers, validation
3. **Schema (schemas/{screen-name}-schema.ts):** Yup validation rules, initial values, types
4. **Styles (views/{screen-name}/styles.ts):** Theme-based StyleSheet
5. **Types (views/{screen-name}/types.ts):** Component props, navigation types, style props
6. **Translations (views/{screen-name}/translations.ts):** i18n keys and values

---

## NAMING CONVENTIONS & STANDARDS

### 1. Import Order
**STRICT ORDER - Must follow this sequence:**
```typescript
// 1. React imports (always first)
import React, {FC, useState, useEffect, useMemo} from 'react';
import {View, Text, StyleSheet} from 'react-native';

// 2. Third-party library imports
import {useNavigation} from '@react-navigation/native';
import {useFormik} from 'formik';

// 3. Custom component imports (after React and third-party)
import * as Components from '@app/components';

// 4. Theme and utilities
import {useNewTheme, Theme, translation, ContextualType} from 'react-core';

// 5. Assets (SVG icons, images)
import {IconName} from 'app/assets/svg';

// 6. Feature-level imports (hooks, schemas) - OUTSIDE view folder
import {useScreenName} from '../../hooks/use-screen-name';
import {ScreenNameSchema, screenNameInitialValues} from '../../schemas/screen-name-schema';

// 7. Local view imports (types, styles)
import {getStyles} from './styles';
import {ScreenNameProps} from './types';
```

### 2. Component ID Naming Convention

**Pattern:** `<<ComponentName>><<FieldName>>`
- Use **TitleCase** for both component name and field name
- No spaces, no underscores, just concatenated TitleCase

**Examples:**
```typescript
// Input components
id="InputTotalExpenses"
id="InputFinancialObligations"
id="InputNickname"

// Label components
id="LabelTitle"
id="LabelDescription"
id="LabelScreenTitle"
id="LabelScreenSubtitle"

// Button components
id="ButtonNext"
id="SubmitButtonNextButton"

// Checkbox components
id="CustomCheckboxDisclosureCheckbox"
id="CheckboxAcknowledgement"

// Screen containers
id="ScreenContainerMonthlyExpensesScreen"
```

### 3. Translation Key Pattern

**Pattern:** `<<Journey>><<ScreenName>><<ComponentAbbreviation>><<FieldName>>`
- All parts in TitleCase, no separators
- Component abbreviation must be in proper case

**Component Abbreviations:**
- `Lbl` = Label
- `Btn` = Button
- `Txt` = Text input value
- `Plc` = Placeholder
- `Chk` = Checkbox
- `Info` = Info/help text
- `Error` = Error message

**Examples:**
```typescript
// Labels
title={t('CreditCardApplicationMonthlyExpensesLblTitle')}
text={t('OnboardingMonthlyExpensesLblSubtitle')}

// Buttons
label={t('OnboardingMonthlyExpensesNextBtnLbl')}

// Placeholders
placeholder={t('OnboardingMonthlyExpensesPlcTotalExpenses')}
placeholder={t('OnboardingMonthlyExpensesPlcFinancialOblgn')}

// Checkboxes
title={t('OnboardingMonthlyExpensesChkTitle')}
linkTitle={t('OnboardingMonthlyExpensesChkLinkTitle')}

// Info text
text={t('OnboardingMonthlyExpensesInfoFinancialOblgn')}

// Total/Summary
text={t('OnboardingMonthlyExpensesLblTotalAmt')}
```

---

## CUSTOM HOOKS PATTERN

### Hook File Structure: `app/features/{feature}/hooks/use-{screen-name}.ts`

**Location:** At feature level, NOT inside view folder

**Purpose:** Centralize all business logic, state management, form handling, and event handlers

**Must Include:**
1. All useState declarations
2. Formik form management
3. useMemo for computed values
4. All event handlers (onChange, onPress, etc.)
5. Validation logic
6. Navigation logic
7. API calls (if any)

**Example Pattern:**
```typescript
###FilePath: app/features/{feature}/hooks/use-{screen-name}.ts

import {useState, useMemo} from 'react';
import {useFormik} from 'formik';
import {useNavigation} from '@react-navigation/native';
import {ScreenNameSchema, screenNameInitialValues} from '../schemas/screen-name-schema';

export const useScreenName = () => {
  // 1. State declarations
  const [fieldOne, setFieldOne] = useState<string>('');
  const [fieldTwo, setFieldTwo] = useState<string>('');
  const [isChecked, setIsChecked] = useState<boolean>(false);

  const navigation = useNavigation();

  // 2. Formik form management
  const formikForm = useFormik({
    validateOnChange: true,
    validateOnBlur: true,
    initialValues: screenNameInitialValues,
    validationSchema: ScreenNameSchema,
    onSubmit: async (values) => {
      // Submit logic here
      console.log('Form submitted:', values);
    },
  });

  // 3. Helper functions (if needed)
  const parseAmount = (amountString: string): number => {
    return parseFloat(amountString.replace(/,/g, '') || '0');
  };

  // 4. Computed values with useMemo
  const isFormValid = useMemo(() => {
    // Validation logic
    return fieldOne !== '' && fieldTwo !== '' && isChecked;
  }, [fieldOne, fieldTwo, isChecked]);

  // 5. Event handlers
  const onChangeFieldOne = (text: string) => {
    setFieldOne(text);
  };

  const onChangeFieldTwo = (text: string) => {
    setFieldTwo(text);
  };

  const onCheckboxSelect = () => {
    setIsChecked(!isChecked);
  };

  const handleNext = () => {
    console.log('Next pressed');
    // navigation.navigate('NextScreen');
  };

  const onBackButtonPress = () => {
    navigation.goBack();
  };

  // 6. Return all state, handlers, and computed values
  return {
    // State
    fieldOne,
    fieldTwo,
    isChecked,

    // Form
    formikForm,

    // Computed
    isFormValid,

    // Handlers
    onChangeFieldOne,
    onChangeFieldTwo,
    onCheckboxSelect,
    handleNext,
    onBackButtonPress,
  };
};
```

---

## VALIDATION SCHEMAS PATTERN

### Schema File Structure: `app/features/{feature}/schemas/{screen-name}-schema.ts`

**Location:** At feature level, NOT inside view folder

**Purpose:** Define Yup validation rules, initial values, and form types

**Must Include:**
1. Yup validation schema
2. Initial values object
3. TypeScript type for form values
4. Import error message keys from constants

**Example Pattern:**
```typescript
###FilePath: app/features/{feature}/schemas/{screen-name}-schema.ts

import {Errors} from '@app/constants';
import * as yup from 'yup';

// 1. Yup Validation Schema
export const ScreenNameSchema = yup.object().shape({
  fieldOne: yup
    .string()
    .min(3, Errors.FieldOneMinLength)
    .max(50, Errors.FieldOneMaxLength)
    .required(Errors.FieldOneRequired),

  fieldTwo: yup
    .string()
    .matches(/^[0-9]+$/, Errors.FieldTwoInvalid)
    .required(Errors.FieldTwoRequired),
});

// 2. Initial Values
export const screenNameInitialValues = {
  fieldOne: '',
  fieldTwo: '',
};

// 3. TypeScript Type
export type ScreenNameInitialValuesType = {
  fieldOne: string;
  fieldTwo: string;
};
```

**Common Validation Patterns:**
```typescript
// Required field
.required(Errors.FieldRequired)

// Min/Max length
.min(3, Errors.MinLength)
.max(50, Errors.MaxLength)

// Regex patterns
.matches(/^[a-zA-Z0-9]+$/, Errors.AlphanumericOnly)
.matches(/^[0-9]+$/, Errors.NumericOnly)

// Email
.email(Errors.InvalidEmail)

// Number validation
yup.number()
  .min(0, Errors.MinValue)
  .max(1000000, Errors.MaxValue)
  .required(Errors.Required)
```

---

## VIEW COMPONENT PATTERN

### View File: `app/features/{feature}/views/{screen-name}/index.tsx`

**Purpose:** Pure UI component - only rendering, no business logic

**Pattern:**
```typescript
###FilePath: app/features/{feature}/views/{screen-name}/index.tsx

// 1. React imports
import React from 'react';
import {View} from 'react-native';

// 2. Third-party imports
// (if needed)

// 3. Custom components
import {
  ScreenContainer,
  Label,
  Input,
  SubmitButton,
  CustomCheckbox,
} from '@app/components';

// 4. Theme and utilities
import {useNewTheme, translation, ContextualType} from 'react-core';

// 5. Assets
import {IconName} from 'app/assets/svg';

// 6. Feature-level imports (hooks, schemas) - TWO LEVELS UP
import {useScreenName} from '../../hooks/use-screen-name';

// 7. Local view imports (types, styles)
import {getStyles} from './styles';
import {ScreenNameProps} from './types';
import {variants} from 'app/components/label/types';

const ScreenName: React.FC<ScreenNameProps> = ({navigation}) => {
  const theme = useNewTheme();
  const styles = getStyles({theme});
  const {t} = translation.useTranslation();

  // Get all state and handlers from custom hook
  const {
    fieldOne,
    fieldTwo,
    isChecked,
    formikForm,
    isFormValid,
    onChangeFieldOne,
    onChangeFieldTwo,
    onCheckboxSelect,
    handleNext,
    onBackButtonPress,
  } = useScreenName();

  return (
    <ScreenContainer
      id="ScreenContainerScreenName"
      showGoBackIcon
      onPressLeftContent={onBackButtonPress}
      bottomScreenContent={
        <View style={styles.bottomContentContainer}>
          <SubmitButton
            id="SubmitButtonNext"
            label={t('JourneyScreenNameBtnNext')}
            onPress={handleNext}
            disabled={!isFormValid}
          />
        </View>
      }>
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.headerContainer}>
          <Label
            id="LabelScreenTitle"
            text={t('JourneyScreenNameLblTitle')}
            variant={variants.titleL}
            style={styles.screenTitle}
          />
          <Label
            id="LabelScreenSubtitle"
            text={t('JourneyScreenNameLblSubtitle')}
            variant={variants.bodyRegularM}
            style={styles.subTitle}
          />
        </View>

        {/* Form Section */}
        <View style={styles.formSection}>
          <Input
            id="InputFieldOne"
            placeholder={t('JourneyScreenNamePlcFieldOne')}
            value={fieldOne}
            setValue={onChangeFieldOne}
            errorText={
              formikForm.touched.fieldOne
                ? formikForm.errors.fieldOne
                : ''
            }
          />

          <Input
            id="InputFieldTwo"
            placeholder={t('JourneyScreenNamePlcFieldTwo')}
            value={fieldTwo}
            setValue={onChangeFieldTwo}
            errorText={
              formikForm.touched.fieldTwo
                ? formikForm.errors.fieldTwo
                : ''
            }
          />
        </View>

        {/* Checkbox */}
        <View style={styles.checkboxContainer}>
          <CustomCheckbox
            id="CustomCheckboxConsent"
            isChecked={isChecked}
            onPress={onCheckboxSelect}
            title={t('JourneyScreenNameChkTitle')}
          />
        </View>
      </View>
    </ScreenContainer>
  );
};

export default ScreenName;
```

---

## 1. COMPONENT MAPPING

{component_mapping}

---

## 2. EXISTING CUSTOM COMPONENTS

{existing_components}

**Usage Instructions:**
- Review all provided component definitions (props, types, usage patterns)
- Match UI elements from the design to these components by type and purpose
- Use these components instead of creating new ones
- Follow the exact prop structures and conventions

---

## 3. SAMPLE WORKING CODE PATTERNS

{sample_code}

**Follow these patterns for:**
- File structure (hooks and schemas at feature level)
- Import statements organization (STRICT ORDER)
- Hook implementation patterns
- Schema validation patterns
- Component composition
- State management through custom hooks
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
1. Analyze the attached design image carefully
2. Identify all UI components, layouts, interactions, text content, and styling
3. Map each visual element to existing custom components
4. Extract exact text content, colors, spacing, and typography
5. Identify form fields that need validation

### Code Structure
Generate files in this format:

```
###FilePath: app/features/{feature}/views/{screen-name}/index.tsx
[View component - UI only, uses custom hook]

###FilePath: app/features/{feature}/hooks/use-{screen-name}.ts
[Custom hook - all business logic, state, handlers]

###FilePath: app/features/{feature}/schemas/{screen-name}-schema.ts
[Yup schema, initial values, types]

###FilePath: app/features/{feature}/views/{screen-name}/styles.ts
[Styles implementation]

###FilePath: app/features/{feature}/views/{screen-name}/types.ts
[Types/interfaces]

###FilePath: app/features/{feature}/views/{screen-name}/translations.ts
[Translation keys with en and ar objects]
```

### Implementation Checklist
- [ ] **Follow STRICT import order** (React → Third-party → Custom → Theme → Assets → Feature imports → Local)
- [ ] **Hooks at feature level:** `app/features/{feature}/hooks/use-{screen-name}.ts`
- [ ] **Schemas at feature level:** `app/features/{feature}/schemas/{screen-name}-schema.ts`
- [ ] **Import hooks with relative path:** `import {useScreenName} from '../../hooks/use-screen-name'`
- [ ] **Import schemas with relative path:** `import {Schema, initialValues} from '../../schemas/screen-name-schema'`
- [ ] **Use TitleCase ID naming:** `ComponentNameFieldName`
- [ ] **Use translation key pattern:** `JourneyScreenNameComponentTypeFieldName`
- [ ] **Separate business logic into custom hook**
- [ ] **Define validation schema** using Yup
- [ ] **View component is pure UI** (no business logic in index.tsx)
- [ ] **All state in custom hook** (useState, useMemo, etc.)
- [ ] **All handlers in custom hook** (onChange, onPress, etc.)
- [ ] **Formik for form management** (in custom hook)
- [ ] **Generate translations.ts** with en and ar objects
- [ ] Use only existing custom components
- [ ] Import components: `import * as Components from '@app/components'`
- [ ] Import theme: `import {useNewTheme, Theme, translation} from 'react-core'`
- [ ] Implement TypeScript types properly
- [ ] Use `getStyles()` pattern with theme
- [ ] Match design precisely

### Hook Development Guidelines
**Custom Hook Must Include:**
1. All useState declarations for form fields and UI state
2. Formik setup with schema and initial values
3. useMemo for computed values (isFormValid, totals, etc.)
4. Helper functions (parseAmount, formatData, etc.)
5. Event handlers (onChange, onPress, onSelect, etc.)
6. Navigation handlers (onBack, onNext, etc.)
7. API call functions (if applicable)
8. Return object with all state, handlers, and computed values

**Hook Return Pattern:**
```typescript
return {
  // State values
  field1,
  field2,
  isChecked,

  // Form
  formikForm,

  // Computed values
  isFormValid,
  totalAmount,

  // Handlers
  onChangeField1,
  onChangeField2,
  onCheckboxSelect,
  handleSubmit,
  onBackPress,
};
```

### Schema Development Guidelines
**Schema Must Include:**
1. Yup validation schema with proper rules
2. Error message keys from Errors constant
3. Initial values object matching schema shape
4. TypeScript type derived from initial values
5. Validation for all required fields
6. Custom validation rules (regex, min/max, etc.)

---

## OUTPUT FORMAT

Provide complete, production-ready code organized by file path:

1. **View component** (views/{screen-name}/index.tsx) - Pure UI using custom hook
2. **Custom hook** (hooks/use-{screen-name}.ts) - All business logic at feature level
3. **Schema** (schemas/{screen-name}-schema.ts) - Yup validation at feature level
4. **Styles** (views/{screen-name}/styles.ts) - Theme-based StyleSheet
5. **Types** (views/{screen-name}/types.ts) - TypeScript interfaces
6. **Translations** (views/{screen-name}/translations.ts) - i18n keys

**File Path Examples:**
```
###FilePath: app/features/credit-card/views/monthly-expenses/index.tsx
###FilePath: app/features/credit-card/hooks/use-monthly-expenses.ts
###FilePath: app/features/credit-card/schemas/monthly-expenses-schema.ts
###FilePath: app/features/credit-card/views/monthly-expenses/styles.ts
###FilePath: app/features/credit-card/views/monthly-expenses/types.ts
###FilePath: app/features/credit-card/views/monthly-expenses/translations.ts
```

**Code must be:**
- Ready to integrate into existing project
- Free of mocks, placeholders, or TODOs
- Following exact patterns from samples
- Using only provided custom components
- Properly separated (UI vs logic)
- Using custom hooks for all business logic at feature level
- Using Yup schemas for all validation at feature level
- Properly typed with TypeScript
- Following all naming conventions
- Using correct import order
- Including proper IDs for all components
- Using translation keys for all text
- Importing hooks and schemas from feature level with correct relative paths

Generate the code now based on the attached design image, following ALL conventions and patterns above.

'''

ENRICH_PROMPT = '''

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

# ENRICH_PROMPT = '''


# You are enhancing React Native code with precise design specifications from Figma API JSON data.


# ---


# ## CONTEXT


# This is **iteration {iteration_number}** of code enrichment. You are refining previously generated code using Figma design data.


# **Input Files:**
# 1. **Current Code** - React Native code from previous iteration (or Step-1 if first iteration)
# 2. **Theme Colors File** - Pre-defined theme color mappings (key-value pairs)
# 3. **Figma Design Image** - Visual reference for the screen
# 4. **Figma API JSON Data** (Part {part_number} of {total_parts}) - Design specifications extracted from Figma


# ---


# ## FILE STRUCTURE REMINDER


# **Your code must follow this structure (from Step-1):**


# app/features/{feature}/
# ├── views/
# │   └── {screen-name}/
# │       ├── index.tsx          # Main view component (UI only)
# │       ├── styles.ts          # StyleSheet definitions
# │       ├── types.ts           # TypeScript interfaces/types
# │       └── translations.ts    # Translation keys (en/ar)
# ├── hooks/
# │   └── use-{screen-name}.ts   # Custom hook (business logic) - FEATURE LEVEL
# └── schemas/
#     └── {screen-name}-schema.ts # Yup validation schema - FEATURE LEVEL


# **Import paths in view component:**
# // Feature-level imports (TWO LEVELS UP from view)
# import {useScreenName} from '../../hooks/use-screen-name';
# import {ScreenNameSchema} from '../../schemas/screen-name-schema';

# // Local view imports
# import {getStyles} from './styles';
# import {ScreenNameProps} from './types';



# ---


# ## CRITICAL INSTRUCTIONS


# ### ❌ DO NOT:
# - Remove or replace custom component imports
# - Create new components or mock implementations
# - **Change file paths or file structure (hooks/schemas stay at feature level)**
# - **Move hooks or schemas into view folder**
# - Alter business logic or state management in hooks
# - Modify validation schemas or form logic
# - Use hardcoded color hex values
# - Change import paths for hooks/schemas


# ### ✅ DO:
# - **Restructure component layout to match Figma design exactly**
# - **Add, remove, or reorder JSX elements to match Figma visual hierarchy**
# - **Change component types (e.g., View to ScrollView) if Figma demands it**
# - **Adjust flex direction, nesting, and container structure per Figma layout**
# - Enrich styles with precise values from Figma API JSON
# - Map Figma colors to existing theme color keys carefully
# - Update padding, margin, spacing, borderRadius from Figma data
# - Apply font families, font sizes, font weights from Figma
# - Add shadows, borders, opacity values from Figma
# - Maintain existing custom component imports (reuse them in new layout)
# - **Keep hooks at feature level:** `app/features/{feature}/hooks/`
# - **Keep schemas at feature level:** `app/features/{feature}/schemas/`
# - Keep file structure: views/{screen}/index.tsx, styles.ts, types.ts, translations.ts
# - Use `theme.colors['theme-key']` for all colors
# - Preserve import paths (../../hooks/, ../../schemas/)


# ---


# ## LAYOUT RESTRUCTURING GUIDELINES


# When the existing code layout differs from the Figma design:


# ### Allowed Structural Changes:
# 1. **Component hierarchy** - Add/remove wrapper Views, adjust nesting depth
# 2. **Layout containers** - Switch between View, ScrollView, FlatList based on Figma structure
# 3. **Element order** - Rearrange JSX elements to match Figma visual sequence
# 4. **Flex direction** - Change from row to column or vice versa per Figma layout
# 5. **Conditional rendering** - Adjust which elements render based on Figma design
# 6. **Grid/List patterns** - Restructure from grid to list or vice versa if Figma shows different pattern


# ### Required Preservation:
# 1. **Custom component imports** - Must reuse all imported custom components (Button, Card, Input, etc.)
#    - ✅ CORRECT: Move `<CustomButton />` to different position in layout
#    - ❌ WRONG: Replace `<CustomButton />` with generic `<TouchableOpacity>`
# 2. **Hook usage** - Keep all hook calls and their logic integration
#    - ✅ CORRECT: Use hook data in restructured JSX
#    - ❌ WRONG: Remove hook calls or ignore their returned values
# 3. **Business logic flow** - Maintain form submissions, navigation, state updates
#    - ✅ CORRECT: Wire restructured form inputs to existing validation
#    - ❌ WRONG: Break form submission flow during restructuring


# ### Restructuring Process:
# 1. Compare existing code structure with Figma design image
# 2. Identify gaps – missing elements, wrong order, incorrect nesting
# 3. Plan restructure – sketch new JSX hierarchy matching Figma
# 4. Preserve integrations – ensure custom components, hooks, schemas still connect properly
# 5. Implement – rewrite JSX structure to match Figma exactly
# 6. Enrich styles – apply Figma design tokens to the new structure


# ---


# ## THEME COLOR MAPPING


# **Available Theme Colors (from theme_colors_common.txt):**


# {theme_colors_content}


# **Color Mapping Rules:**
# 1. **Extract color from Figma JSON** - Look for color values in RGB, RGBA, or hex format
# 2. **Find closest theme match** - Match Figma color to the closest existing theme key
# 3. **Use theme key in code** - Replace with `theme.colors['theme-key-name']`
# 4. **Priority mapping:**
#    - Background colors → `background-01` to `background-04`
#    - Surface colors → `surface-*` variations
#    - Text colors → `content-primary`, `content-secondary`, `content-tertiary`
#    - Interactive elements → `surface-interactive-*` or `content-interactive-*`
#    - Borders → `border-*` variations
#    - Icons → `icon-*` variations


# **Example Mapping:**


# Figma: {"r": 0.098, "g": 0.027, "b": 0.290, "a": 1} → #19074A → primary-100  
# Code: backgroundColor: theme.colors['background-04'] // maps to primary-100


# Figma: {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1} → #FFFFFF → neutral-00  
# Code: color: theme.colors['content-inverted-primary'] // white text


# ---


# ## FIGMA API JSON ANALYSIS


# **From the provided Figma JSON data, extract and apply:**


# ### 1. **Layout & Spacing**
# - `paddingLeft`, `paddingRight`, `paddingTop`, `paddingBottom`
# - `itemSpacing` (gap between flex children)
# - `layoutMode` (HORIZONTAL, VERTICAL)
# - `primaryAxisAlignItems` (flex alignment)
# - `counterAxisAlignItems` (cross-axis alignment)
# - `layoutGrow` (flex grow)
# - `layoutAlign` (stretch, center, etc.)


# ### 2. **Typography**
# - `fontFamily` (map to closest available system font or custom font)
# - `fontSize`
# - `fontWeight` (100-900)
# - `lineHeightPx` or `lineHeightPercent`
# - `letterSpacing`
# - `textAlignHorizontal` (LEFT, CENTER, RIGHT)
# - `textAlignVertical` (TOP, CENTER, BOTTOM)
# - `textCase` (UPPER, LOWER, TITLE)


# ### 3. **Colors**
# - `fills` array (background colors, gradient fills)
# - `strokes` array (border colors)
# - `color` (text color)
# - Map ALL colors to theme keys - NEVER use raw hex/RGB values


# ### 4. **Visual Effects**
# - `cornerRadius` or `rectangleCornerRadii` (border radius)
# - `effects` array (shadows, blurs)
#   - `type`: DROP_SHADOW, INNER_SHADOW, LAYER_BLUR
#   - `color`, `offset`, `radius`, `spread`
# - `opacity`
# - `strokeWeight` (border width)


# ### 5. **Constraints & Sizing**
# - `constraints` (min/max width, height)
# - `minWidth`, `maxWidth`, `minHeight`, `maxHeight`
# - `layoutSizingHorizontal`, `layoutSizingVertical` (FIXED, HUG, FILL)


# ---


# ## ENRICHMENT PROCESS


# ### Step 1: Identify Components in Figma JSON
# - Match Figma layer names to React Native components in view
# - Find corresponding nodes in JSON by `name`, `id`, or `type`
# - Note which file each enrichment applies to (view, styles, hooks, schemas)


# ### Step 2: Extract Design Properties
# - For each matched component, extract all relevant properties
# - Note down values for spacing, colors, typography, effects
# - **Focus on styles.ts enrichment** - business logic stays in hooks


# ### Step 3: Map Colors to Theme
# - Convert Figma color values to theme keys
# - Document mapping decisions inline with comments
# - Example: `// Figma: #19074A → primary-100 → background-04`


# ### Step 4: Update Styles
# - Apply extracted values to StyleSheet in `styles.ts`
# - Update `getStyles()` function with precise measurements
# - Add responsive considerations if needed
# - **Do not modify hooks or schemas** unless Figma reveals new validation requirements


# ### Step 5: Validate File Structure
# - Ensure hooks remain at: `app/features/{feature}/hooks/use-{screen-name}.ts`
# - Ensure schemas remain at: `app/features/{feature}/schemas/{screen-name}-schema.ts`
# - Verify import paths are correct (../../hooks/, ../../schemas/)
# - Check all files maintain their separation of concerns


# ---


# ## OUTPUT FORMAT


# Provide the enriched code maintaining the EXACT file structure from Step-1:


# ###FilePath: app/features/{feature}/views/{screen-name}/index.tsx
# [Component implementation – may have restructured layout to match Figma]
# [Import hooks from: ../../hooks/use-{screen-name}]
# [Import schemas from: ../../schemas/{screen-name}-schema]


# ###FilePath: app/features/{feature}/hooks/use-{screen-name}.ts
# [Custom hook – typically unchanged unless new business logic needed]
# [Keep at FEATURE LEVEL, not in view folder]


# ###FilePath: app/features/{feature}/schemas/{screen-name}-schema.ts
# [Validation schema – typically unchanged unless new validation rules needed]
# [Keep at FEATURE LEVEL, not in view folder]


# ###FilePath: app/features/{feature}/views/{screen-name}/styles.ts
# [ENRICHED styles with Figma values and theme color mappings]
# [Most enrichment happens here]


# ###FilePath: app/features/{feature}/views/{screen-name}/types.ts
# [Types/interfaces – add any design-specific types if needed]


# ###FilePath: app/features/{feature}/views/{screen-name}/translations.ts
# [Translation keys – typically unchanged unless new text discovered in Figma]


# ---


# ## ENRICHMENT CHECKLIST


# For each component/element, verify:
# - [ ] **Component structure matches Figma visual hierarchy**
# - [ ] **Element order matches Figma design sequence**
# - [ ] **Layout containers (View/ScrollView/etc.) match Figma behavior**
# - [ ] All custom component imports are reused in new structure
# - [ ] Background color mapped to theme key (from Figma `fills`)
# - [ ] Text color mapped to theme key (from Figma `color`)
# - [ ] Border color mapped to theme key (from Figma `strokes`)
# - [ ] Padding values applied (from Figma `padding*`)
# - [ ] Margin/spacing applied (from Figma `itemSpacing`)
# - [ ] Font family applied (from Figma `fontFamily`)
# - [ ] Font size applied (from Figma `fontSize`)
# - [ ] Font weight applied (from Figma `fontWeight`)
# - [ ] Line height applied (from Figma `lineHeight*`)
# - [ ] Border radius applied (from Figma `cornerRadius`)
# - [ ] Shadows applied (from Figma `effects`)
# - [ ] Opacity applied if < 1 (from Figma `opacity`)
# - [ ] Alignment/justification applied (from Figma layout properties)
# - [ ] **Hooks remain at feature level** (not moved into view)
# - [ ] **Schemas remain at feature level** (not moved into view)
# - [ ] **Import paths preserved** (../../hooks/, ../../schemas/)
# - [ ] **Business logic connections maintained** (form validation, navigation, state)


# ---


# ## SPECIAL NOTES FOR ITERATIVE ENRICHMENT


# **Iteration {iteration_number} Focus:**
# - This is part {part_number} of {total_parts} of Figma JSON data
# - Focus on enriching components/sections covered in this JSON chunk
# - Preserve all enrichments from previous iterations
# - Build upon (don't overwrite) previously refined styles and layout
# - If a property or layout was already enriched in a previous iteration, keep it unless this iteration provides more specific data
# - **Always maintain file structure** - hooks and schemas at feature level


# **Handling Conflicts:**
# - If current Figma data conflicts with previous iteration, use the MORE SPECIFIC value
# - Document any conflicts in inline comments
# - Prioritize visual accuracy to the Figma design image
# - **Never change file locations or import paths**


# **File Structure Validation:**
# - After enrichment, verify:
#   - ✅ Hooks are at: `app/features/{feature}/hooks/`
#   - ✅ Schemas are at: `app/features/{feature}/schemas/`
#   - ✅ View files are at: `app/features/{feature}/views/{screen-name}/`
#   - ✅ Import paths use `../../hooks/` and `../../schemas/`
#   - ✅ No business logic leaked into view component


# ---


# ## WHAT TYPICALLY GETS ENRICHED


# **High Frequency (Almost Every Iteration):**
# - `styles.ts` - Colors, spacing, typography, shadows, borders
# - `index.tsx` - Layout restructuring and style prop values


# **Medium Frequency (Sometimes):**
# - `types.ts` - New style prop interfaces if Figma reveals complex patterns
# - `translations.ts` - New text if Figma has content not in Step-1 code


# **Low Frequency (Rarely):**
# - `hooks/use-{screen-name}.ts` - Only if Figma reveals new business rules
# - `schemas/{screen-name}-schema.ts` - Only if Figma reveals new validation requirements


# **Focus most of the enrichment on `styles.ts` and layout in `index.tsx` to match the Figma design precisely.**


# ---


# ## INPUTS


# **Current Code (from previous iteration):**
# {current_code}


# **Figma API JSON Data (Part {part_number}):**
# {figma_json_chunk}


# **Figma Design Image Reference:**
# [Attached]


# ---


# ## TASK


# Enrich and, if needed, restructure the current code so that the screen visually matches the provided Figma design as closely as possible.


# **Key Requirements:**
# 1. ✅ Match layout and visual hierarchy to Figma
# 2. ✅ Maintain file structure (hooks/schemas at feature level)
# 3. ✅ Preserve import paths (../../hooks/, ../../schemas/)
# 4. ✅ Focus enrichment on styles.ts and layout in index.tsx
# 5. ✅ Map all colors to theme keys
# 6. ✅ Apply precise Figma measurements
# 7. ✅ Keep business logic in hooks unchanged (unless absolutely necessary)
# 8. ✅ Keep validation in schemas unchanged (unless new rules found)
# 9. ✅ Document color mappings with inline comments
# 10. ✅ Preserve all custom component imports and reuse them in the new layout


# Output the complete enriched code ready for the next iteration or final integration, with proper file structure and import paths maintained, and with layout aligned to the Figma design.


# '''
