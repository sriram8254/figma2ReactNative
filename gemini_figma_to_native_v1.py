from google import genai
import base64
import json

client=genai.Client(api_key='AIzaSyC_j2IYqbRgJVs7K-bfcAOFodz1NGhI8Yw')
# client=genai.Client(api_key='AIzaSyBElqYzVOzK43qWbOsdE9EULTlfof9qhKQ')


def load_image(imgpath):
    with open(imgpath,'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

user_stories_file_content=''
component_mapping = ''
existing_components = ''
sample_code = ''
package_structure = ''
user_stories_file_content=''

component_mapping_file=r'C:\Solutions\figma user story trial\input_folder\gib_mobile\component_mapping_personal_details.txt'
with open(component_mapping_file,'r',encoding='utf-8') as f:
  component_mapping=f.read()

existing_components_file=r'C:\Solutions\figma user story trial\input_folder\gib_mobile\existing_components_personal_details.txt'
with open(existing_components_file,'r',encoding='utf-8') as f:
  existing_components=f.read()  

sample_code_file=r'C:\Solutions\figma user story trial\input_folder\gib_mobile\sample_code_common.txt'
with open(sample_code_file,'r',encoding='utf-8') as f:
  sample_code=f.read()

package_structure_file=r'C:\Solutions\figma user story trial\input_folder\gib_mobile\package_structure_common.txt'
with open(package_structure_file,'r',encoding='utf-8') as f:
  package_structure=f.read()

user_stories_file=r'C:\Solutions\figma user story trial\input_folder\gib_mobile\user_stories_credit_card.txt'
with open(user_stories_file,'r',encoding='utf-8') as f:
  user_stories_file_content=f.read()

prompt_template = '''

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


# final_prompt = prompt_template.replace('{api_json_doc}', api_json_doc)
final_prompt = prompt_template.replace('{user_stories_file_content}', user_stories_file_content)
final_prompt = final_prompt.replace('{component_mapping}', component_mapping)
final_prompt = final_prompt.replace('{existing_components}', existing_components)
final_prompt = final_prompt.replace('{sample_code}', sample_code)
final_prompt = final_prompt.replace('{package_structure}', package_structure)

print(final_prompt)


with open(r'C:\Solutions\figma user story trial\output_folder\gib_mobile\mobile_version_final_prompt.txt','w', encoding='utf-8', errors='ignore') as f:
  f.write(final_prompt)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      genai.types.Part.from_bytes(
        data=load_image(r'C:\Solutions\figma user story trial\input_folder\gib_mobile\personaldetails.png'),
        mime_type='image/png',
      ),
       final_prompt]
  )
print(response.text)

with open(r'C:\Solutions\figma user story trial\output_folder\gib_mobile\mobile_version_native_v1.txt','w', encoding='utf-8', errors='ignore') as f:
  f.write(response.text)