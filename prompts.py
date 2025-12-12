GENERATE_PROMPT = '''


Generate React Native screen code from the attached design image for integration into an existing project.


**Project Configuration:**
- React: 19.1.1
- React Native: 0.82.1
- Gradle: 9.0.0
- TypeScript: Required
- Path Aliases: Configured in babel.config.js


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
- Hardcode comparison values (use Enums/constants instead)
- Misalign flex-direction, justify-content, align-items
- Use incorrect variant capitalization (TitleL, bodyregular, bodySemibold)
- Use separators in variants (body_medium_s, body-medium-s)
- Hardcode fontSize instead of using variants
- Guess variant names without checking the format


**DO:**
- Use existing custom components with proper import statements
- Use direct component imports: `import {Label, Input} from '@app/components'`
- Use path aliases (@app, @features) for all non-local imports
- Use direct component syntax: `<Label>` instead of `<Components.Label>`
- Follow the existing project structure and patterns
- Generate production-ready, integration-ready code
- Use proper file path format: `###FilePath: app/features/{feature}/views/{screen-name}/index.tsx`
- Separate business logic into custom hooks
- Define validation schemas using Yup
- Use Formik for form management
- Match the Figma design structure, layout, spacing, and alignment as closely as possible
- Pay careful attention to flex-direction (row vs column) based on visual design
- Ensure all styles are correctly typed for React Native (ViewStyle, TextStyle, ImageStyle, etc.)
- Use standard React Native StyleSheet.create() only
- Use number literals for all spacing (paddingTop: 20, not '20@vs')
- Keep styles in separate styles.ts file
- Use typed StyleSheet interface (interface Styles {...})
- Import StyleSheet from 'react-native', not third-party packages
- Export components using the screen name as component name in index.tsx
- Identify correct export pattern (export const vs export default) and import accordingly
- Define Enums and typed constants in separate constants.ts file when comparisons are needed
- Define all function arguments and object types in types.ts file
- Verify flex layout directions match the visual design (row for horizontal, column for vertical)
- Use correct variant type case format (variants.bodyMediumM, not variants.bodymediumm)
- Capitalize weight in variants (Regular, Medium, SemiBold, Bold)
- Use uppercase for size in variants (XS, S, M, L, XL)
- Map Figma font specs to correct variant format
- Start variant with lowercase style (titleL, bodyRegularM, not TitleL)


---

## FILE STRUCTURE & ARCHITECTURE


**IMPORTANT:** Hooks and Schemas are at the **feature level**, NOT inside the view folder.


app/features/{feature}/
├── views/
│ └── {screen-name}/
│ ├── index.tsx # Component exported with screen name
│ ├── styles.ts # StyleSheet definitions
│ ├── types.ts # TypeScript interfaces/types
│ ├── translations.ts # Translation keys (en/ar)
│ └── constants.ts # Enums, typed constants (only if needed)
├── hooks/
│ └── use-{screen-name}.ts # Custom hook (business logic, state, handlers)
├── schemas/
│ └── {screen-name}-schema.ts # Yup validation schema & initial values
├── queries/ # API queries/mutations (feature level)
│ └── use-{endpoint-name}-query.ts
├── types/ # Feature-level API types
│ └── {endpoint-name}.types.ts
└── constants/ # Feature-level API constants
└── {endpoint-name}.constants.ts

text


**Example Structure:**


app/features/credit-card/
├── views/
│ ├── monthly-expenses/
│ │ ├── index.tsx
│ │ ├── styles.ts
│ │ ├── types.ts
│ │ ├── translations.ts
│ │ └── constants.ts
│ └── personal-details/
│ ├── index.tsx
│ ├── styles.ts
│ ├── types.ts
│ └── translations.ts
├── hooks/
│ ├── use-monthly-expenses.ts
│ └── use-personal-details.ts
├── schemas/
│ ├── monthly-expenses-schema.ts
│ └── personal-details-schema.ts
├── queries/
│ └── use-profit-rate-inquiry-query.ts
├── types/
│ └── profit-rate-inquiry.types.ts
└── constants/
└── profit-rate-inquiry.constants.ts

text


### Architecture Principles:


1. **View (views/{screen-name}/index.tsx):** Pure UI component, no business logic
2. **Hook (hooks/use-{screen-name}.ts):** All state, logic, handlers, validation and API interaction
3. **Schema (schemas/{screen-name}-schema.ts):** Yup validation rules, initial values, types
4. **Styles (views/{screen-name}/styles.ts):** Theme-based StyleSheet with proper TypeScript typing
5. **Types (views/{screen-name}/types.ts):** Component props, navigation types, function args, object types
6. **Translations (views/{screen-name}/translations.ts):** i18n keys and values
7. **Constants (views/{screen-name}/constants.ts):** Enums, typed constants for comparisons (only if needed)
8. **API Queries (queries/use-{endpoint-name}-query.ts):** RTK Query endpoints for feature APIs
9. **API Types (types/{endpoint-name}.types.ts):** Request/response types for feature APIs
10. **API Constants (constants/{endpoint-name}.constants.ts):** API endpoints, enums, config


---

## PATH ALIASES & BABEL CONFIG


The project uses **babel.config.js** for path alias configuration:


alias: {
tests: ['./tests/'],
'@app': './app',
}

text


**Available Path Aliases:**
- `@app/*` → `app/*`
- `@app/features/*` → `app/features/*`
- `@app/components` → `app/components`
- `@app/assets/svg` → `app/assets/svg`
- `@app/constants` → `app/constants`


**Import Priority Rules:**

1. ✅ Use `@app/features/{feature}/hooks/use-screen-name` for hooks
2. ✅ Use `@app/features/{feature}/schemas/screen-name-schema` for schemas
3. ✅ Use `@app/features/{feature}/queries/use-{endpoint-name}-query` for API queries
4. ✅ Use `@app/features/{feature}/types/{endpoint-name}.types` for API types
5. ✅ Use `@app/features/{feature}/constants/{endpoint-name}.constants` for API constants
6. ✅ Use `@app/components` for shared UI components
7. ✅ Use `@app/assets/svg` for icons and SVGs
8. ✅ Use `@app/constants` for shared app-level constants
9. ❌ Avoid `../../hooks/use-screen-name` when a path alias is available
10. ❌ Avoid `import * as Components from '@app/components'`
11. ✅ Only use relative imports for local view-level files like `./styles`, `./types`, `./translations`, `./constants`


---

## EXPORT/IMPORT PATTERN IDENTIFICATION

**Identify the correct export pattern from existing code and use matching imports:**

### Export Patterns:

**Pattern 1: Named Export**
```typescript
// index.tsx
export const ScreenName: React.FC<ScreenNameProps> = ({navigation}) => {
  // ...
};

// Import elsewhere
import {ScreenName} from '@app/features/feature-name/views/screen-name';
```

**Pattern 2: Default Export**
```typescript
// index.tsx
const ScreenName: React.FC<ScreenNameProps> = ({navigation}) => {
  // ...
};

export default ScreenName;

// Import elsewhere
import ScreenName from '@app/features/feature-name/views/screen-name';
```

**Rules:**
1. **Check existing code patterns** to determine which export style is used
2. **Component name** should match the screen name in TitleCase
3. **Use consistent export style** throughout the same feature
4. **Import accordingly**: Named exports use `{}`, default exports don't

---

## ENUMS & CONSTANTS PATTERN

**Create constants.ts ONLY when comparisons or typed values are needed**

### When to Create constants.ts:
- Status comparisons (e.g., 'active', 'pending', 'completed')
- Type discriminators (e.g., 'error', 'warning', 'success')
- Fixed dropdown options
- Payment methods, card types, etc.
- Any hardcoded string/number used in multiple conditions

### constants.ts Pattern:

```typescript
###FilePath: app/features/{feature}/views/{screen-name}/constants.ts

// Enums for type-safe comparisons
export enum PaymentStatus {
  PAID = 'paid',
  FAILED = 'failed',
  PENDING = 'pending',
}

export enum InstallmentStatus {
  ACTIVE = 'active',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

export enum TagType {
  ERROR = 'error',
  SUCCESS = 'success',
  WARNING = 'warning',
  INFO = 'info',
}

// Typed constants
export const MIN_AMOUNT = 100;
export const MAX_AMOUNT = 100000;

export const PAYMENT_STATUSES = {
  PAID: 'paid' as const,
  FAILED: 'failed' as const,
  PENDING: 'pending' as const,
} as const;

export type PaymentStatusType = typeof PAYMENT_STATUSES[keyof typeof PAYMENT_STATUSES];
```

### Usage in Code:

**❌ WRONG - Hardcoded strings:**
```typescript
if (payment.status === 'paid') {  // Bad
  return <TickIcon />;
}
```

**✅ CORRECT - Using Enums:**
```typescript
import {PaymentStatus} from './constants';

if (payment.status === PaymentStatus.PAID) {  // Good
  return <TickIcon />;
}
```

---

## API INTEGRATION PATTERN (NEW)


**Goal:** Use `api_endpoints` input to generate feature-level API types, queries, and constants, and integrate them into hooks. Use mock implementations initially, but always create placeholders for the actual endpoints.

### 1. api_endpoints Input

You will receive an `api_endpoints` description (for example, from OpenAPI YAML like `accounts.yaml` and `profit-rate-inquiry.yaml`) that defines:

- Paths and HTTP methods (e.g., `/accounts/profit-rate-inquiry` with POST)
- Request schemas (e.g., `profit-rate-inquiry-req`)
- Response schemas (e.g., `profit-rate-inquiry-res`)
- Shared field definitions (e.g., `productType`, `isSuccess`, `currencyName`, etc.)

Use this information to:

- Create strongly typed request/response interfaces
- Create feature-level API constants for endpoints and enums
- Create RTK Query endpoints in `queries` folder
- Wire these into the feature hook


### 2. API Types File Pattern

**Location:**
`app/features/{feature}/types/{endpoint-name}.types.ts`

**Purpose:**
Define all API request/response types derived from the `api_endpoints` specification.

**Example (based on profit-rate-inquiry):**

###FilePath: app/features/accounts/types/profit-rate-inquiry.types.ts

export interface ProfitRateInquiryRequest {
productType: string;
}

export interface ProfitRateItem {
currencyCode: string;
depositQuarter: string;
depositRate: string;
depositYear: string;
fromAmount: string;
toAmount: string;
isRecommendedRate: boolean;
productId: string;
tenure: number;
}

export interface ProfitRateInquiryResponse {
isSuccess: boolean;
lastUpdatedOn: string;
profitRateList: ProfitRateItem[];
}

text


### 3. API Constants File Pattern

**Location:**
`app/features/{feature}/constants/{endpoint-name}.constants.ts`

**Purpose:**
Define API-related constants (endpoint paths, enums, config).

###FilePath: app/features/accounts/constants/profit-rate-inquiry.constants.ts

export const API_ENDPOINTS = {
PROFIT_RATE_INQUIRY: '/accounts/profit-rate-inquiry', // placeholder for actual endpoint
} as const;

export enum ProductType {
RTDEP = 'RTDEP',
// Add other product types if present in api_endpoints
}

export const API_CONFIG = {
BASE_URL: 'http://0.0.0.0:8080/v1/api', // placeholder base URL
TIMEOUT: 30000,
RETRY_COUNT: 3,
} as const;

text


### 4. API Query File Pattern

**Location:**
`app/features/{feature}/queries/use-{endpoint-name}-query.ts`

**Purpose:**
Define RTK Query API endpoints using the types and constants.

###FilePath: app/features/accounts/queries/use-profit-rate-inquiry-query.ts

import {BaseQueryFn, FetchArgs, fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {createApi} from '@reduxjs/toolkit/query/react';
import {
ProfitRateInquiryRequest,
ProfitRateInquiryResponse,
} from '@app/features/accounts/types/profit-rate-inquiry.types';
import {API_CONFIG, API_ENDPOINTS} from '@app/features/accounts/constants/profit-rate-inquiry.constants';

const baseQuery = fetchBaseQuery({
baseUrl: API_CONFIG.BASE_URL,
});

export const accountsApi = createApi({
reducerPath: 'accountsApi',
baseQuery,
endpoints: builder => ({
profitRateInquiry: builder.mutation<ProfitRateInquiryResponse, ProfitRateInquiryRequest>({
query: body => ({
url: API_ENDPOINTS.PROFIT_RATE_INQUIRY, // placeholder for actual endpoint
method: 'POST',
body,
// headers will be injected from hook via getHeaders wrapper
}),
}),
}),
});

export const {useProfitRateInquiryMutation} = accountsApi;

text


### 5. Hook Integration Pattern

**Location:**
`app/features/{feature}/hooks/use-{screen-name}.ts`

**Purpose:**
Use the generated query and types inside the feature hook, with mock behavior initially and easy switch to real API.

###FilePath: app/features/accounts/hooks/use-profit-rate-screen.ts

import {useEffect, useState} from 'react';
import {useHeaders} from '@app/features/authentication/hooks';
import {usePostLoginHandler} from 'app/hooks/post-login-handler';
import {
ProfitRateInquiryRequest,
ProfitRateInquiryResponse,
} from '@app/features/accounts/types/profit-rate-inquiry.types';
import {useProfitRateInquiryMutation} from '@app/features/accounts/queries/use-profit-rate-inquiry-query';
import {ProductType} from '@app/features/accounts/constants/profit-rate-inquiry.constants';

export const useProfitRateScreen = () => {
const {getHeaders} = useHeaders();

const {
action: profitRateInquiryAction,
data: profitRateInquiryResponse,
error: profitRateInquiryError,
} = usePostLoginHandler(useProfitRateInquiryMutation);

const [isLoading, setIsLoading] = useState(false);
const [profitRates, setProfitRates] = useState<ProfitRateInquiryResponse | null>(null);

// Mock implementation using api_endpoints examples
const fetchProfitRatesMock = async () => {
setIsLoading(true);

text
const mockResponse: ProfitRateInquiryResponse = {
  isSuccess: true,
  lastUpdatedOn: '2025-04-28 12:06:13',
  profitRateList: [
    {
      currencyCode: 'USD',
      depositQuarter: '1',
      depositRate: '3.5',
      depositYear: '2025',
      fromAmount: '5000',
      toAmount: '50000',
      isRecommendedRate: false,
      productId: 'RTDEP',
      tenure: 30,
    },
  ],
};

// NOTE: Currently using mock data derived from api_endpoints examples.
// When real backend is ready, switch to fetchProfitRatesReal()
setTimeout(() => {
  setProfitRates(mockResponse);
  setIsLoading(false);
}, 500);
};

// Real API implementation using RTK Query
const fetchProfitRatesReal = () => {
const options: ProfitRateInquiryRequest = {
productType: ProductType.RTDEP,
};

text
const headers = getHeaders({screenId: 'ProfitRateScreen'});

// usePostLoginHandler wraps RTK Query mutation
profitRateInquiryAction({
  headers,
  request: options,
} as any);
};

useEffect(() => {
if (profitRateInquiryResponse?.isSuccess) {
setProfitRates(profitRateInquiryResponse);
}
}, [profitRateInquiryResponse, profitRateInquiryError]);

return {
profitRates,
isLoading,
fetchProfitRatesMock,
fetchProfitRatesReal,
};
};

text


### 6. View Integration Pattern

In the view (`index.tsx`), call the hook methods and show loading/data using existing components:

// inside Screen component body
const {
profitRates,
isLoading,
fetchProfitRatesMock,
fetchProfitRatesReal,
} = useProfitRateScreen();

// example usage in JSX
<SubmitButton
id="SubmitButtonFetchProfitRates"
label={t('AccountsProfitRateScreenBtnFetch')}
onPress={fetchProfitRatesMock}
/>

// Render profitRates list using Label, InfoCard, etc.

text


### 7. API Integration Checklist

- [ ] Parse `api_endpoints` to identify paths, methods, and schemas
- [ ] Generate request/response interfaces in `types/{endpoint-name}.types.ts`
- [ ] Generate API constants (endpoints, enums) in `constants/{endpoint-name}.constants.ts`
- [ ] Generate RTK Query API definition in `queries/use-{endpoint-name}-query.ts`
- [ ] Use mock implementation in hooks using example objects from `api_endpoints`
- [ ] Provide separate real implementation that uses `usePostLoginHandler` + RTK Query
- [ ] Always keep endpoint strings in constants (no hardcoded URLs in hooks/views)
- [ ] Use path aliases for all API-related imports
- [ ] Never place API types/queries/constants inside view folder


---

## TYPES.TS REQUIREMENTS

**Define ALL function arguments, object types, and interfaces in types.ts**

### What Goes in types.ts:

```typescript
###FilePath: app/features/{feature}/views/{screen-name}/types.ts

import {NativeStackNavigationProp} from '@react-navigation/native-stack';
import {PaymentStatus, InstallmentStatus} from './constants';

// Component props
export interface ScreenNameProps {
  navigation: NativeStackNavigationProp<any>;
}

// Data types
export interface PaymentItem {
  amount: number;
  date: string;
  status: PaymentStatus;  // Use enum type
}

export interface InstallmentData {
  installmentStatus: InstallmentStatus;
  merchantName: string;
  merchantLogoUri: string;
  totalAmount: number;
  paidAmount: number;
  remainingAmount: number;
  startDate: string;
  endDate: string;
  payments: PaymentItem[];
}

// Function argument types
export interface FormatAmountArgs {
  amount: number;
  currency: string;
  locale?: string;
}

export interface CalculateTotalArgs {
  payments: PaymentItem[];
  includeStatus?: PaymentStatus[];
}

// Event handler types
export type OnPaymentSelectHandler = (payment: PaymentItem) => void;
export type OnStatusChangeHandler = (status: InstallmentStatus) => void;

// Utility types
export type AmountFormatter = (args: FormatAmountArgs) => string;
export type TotalCalculator = (args: CalculateTotalArgs) => number;
```

**Rules:**
1. ✅ Define all interfaces and types used in the view
2. ✅ Define function argument object types
3. ✅ Define event handler types
4. ✅ Use enum types from constants.ts
5. ✅ Export all types for use in hooks and other files
6. ❌ Don't include StyleProp wrappers (handled by components)

---

## LAYOUT ALIGNMENT REQUIREMENTS

**CRITICAL: Pay attention to flex-direction based on visual design**

### Flex Direction Rules:

**Analyze the design image to determine layout direction:**

1. **Horizontal Layout** (side-by-side elements):
   ```typescript
   container: {
     flexDirection: 'row',           // Elements in a row
     justifyContent: 'space-between', // Horizontal spacing
     alignItems: 'center',            // Vertical alignment
   }
   ```

2. **Vertical Layout** (stacked elements):
   ```typescript
   container: {
     flexDirection: 'column',         // Elements stacked (default)
     justifyContent: 'flex-start',    // Vertical spacing
     alignItems: 'flex-start',        // Horizontal alignment
   }
   ```

### Common Layout Patterns:

**Two-column layout (side-by-side):**
```typescript
<View style={styles.rowContainer}>
  <View style={styles.leftColumn}>
    <Label text="From" />
    <Label text="23 Dec, 2024" />
  </View>
  <View style={styles.rightColumn}>
    <Label text="To" />
    <Label text="08 Jul, 2025" />
  </View>
</View>

// Styles
rowContainer: {
  flexDirection: 'row',              // ← CRITICAL: row for side-by-side
  justifyContent: 'space-between',
  gap: 16,
}
```

**Vertical list (stacked items):**
```typescript
<View style={styles.listContainer}>
  <View style={styles.listItem}>
    <Label text="Item 1" />
  </View>
  <View style={styles.listItem}>
    <Label text="Item 2" />
  </View>
</View>

// Styles
listContainer: {
  flexDirection: 'column',           // ← CRITICAL: column for stacking
  gap: 12,
}
```

### Layout Checklist:
- [ ] Analyze if elements are side-by-side (row) or stacked (column)
- [ ] Set flexDirection correctly based on visual layout
- [ ] Use justifyContent for main axis spacing
- [ ] Use alignItems for cross axis alignment
- [ ] Test that layout matches Figma design structure

---

## NAMING CONVENTIONS & STANDARDS

{conventions_and_standards}

(Above content includes: strict import order, component ID naming, translation key patterns, hook & schema patterns, TypeScript style guidelines, and proper export patterns.)

---

## TYPESCRIPT & STYLE PROP REQUIREMENTS

**Goal:** Ensure correct typing of all styles and style props for React Native components.

### General Rules

- Do **not** define a `StyleProps` interface in `types.ts` that wraps styles in `StyleProp<T>`.
- Define raw styles (ViewStyle, TextStyle, ImageStyle) in `styles.ts` and type `StyleSheet.create` with a `Styles` interface.
- Component props that accept styles (like `Label.style`) should be typed as `StyleProp<TextStyle>` etc. in the component definition (already done in existing components).
- Passing `styles.someTextStyle` (type `TextStyle`) into a prop of type `StyleProp<TextStyle>` is valid and expected.

### In types.ts

```typescript
import {NativeStackNavigationProp} from '@react-navigation/native-stack';

export interface ScreenNameProps {
  navigation: NativeStackNavigationProp<any>;
  // Add other non-style props if needed
}

// Define all function argument types
export interface CalculateArgs {
  amount: number;
  percentage: number;
}

// Define all object types used in the component
export interface UserData {
  name: string;
  email: string;
  age: number;
}
```

### In styles.ts

```typescript
import {StyleSheet, ViewStyle, TextStyle} from 'react-native';
import {Theme} from 'react-core';

interface Styles {
  container: ViewStyle;
  headerContainer: ViewStyle;
  rowContainer: ViewStyle;           // For flex-row layouts
  columnContainer: ViewStyle;        // For flex-column layouts
  sectionTitle: TextStyle;
  dateLabel: TextStyle;
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
    rowContainer: {
      flexDirection: 'row',          // Horizontal layout
      justifyContent: 'space-between',
      alignItems: 'center',
      gap: 16,
    },
    columnContainer: {
      flexDirection: 'column',       // Vertical layout
      gap: 12,
    },
    sectionTitle: {
      fontSize: 16,
      fontWeight: '600',
      color: theme.colors['content-primary'],
    },
    dateLabel: {
      fontSize: 14,
      color: theme.colors['content-secondary'],
    },
  });
};
```

**Example usage in View:**

```typescript
<Label
  id="LabelInstallmentFrom"
  text={t('MeemAshalInstallmentsLblFrom')}
  variant={variants.bodyRegularS}
  style={styles.dateLabel}  // Label.style is StyleProp<TextStyle>
/>
```

---

## DESIGN MATCHING REQUIREMENTS

**CRITICAL: Match the Figma design structure, layout, spacing, and alignment as closely as possible.**

When analyzing the attached Figma design image:

1. **Layout Structure:** Replicate the exact component hierarchy (containers, sections, cards, rows, etc.).
2. **Flex Direction:** Identify if elements are side-by-side (row) or stacked (column) and set flexDirection accordingly.
3. **Spacing:** Match margins, paddings, gaps, and spacing between elements.
4. **Alignment:** Preserve all horizontal and vertical alignments (justifyContent, alignItems).
5. **Typography:** Respect font size, weight, color, and line-height.
6. **Colors:** Use theme colors that correspond to the design palette.
7. **Sizing:** Match widths, heights, and flex settings where visible.
8. **Visual Hierarchy:** Maintain the same grouping and emphasis as the design.

**Layout Checklist:**

- [ ] Main container type identified (e.g., ScreenContainer, ScrollView, etc.)
- [ ] Header and title areas structured correctly
- [ ] Form sections grouped as in design
- [ ] Flex-direction set correctly (row vs column) for each container
- [ ] Buttons placed correctly (bottom fixed, inline, etc.)
- [ ] Any decorative or informational components (cards, tags, chips) mapped to existing components
- [ ] Icons and images placed and sized as in Figma
- [ ] Spacing matches design (margins, paddings, gaps)

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
- Export patterns (named vs default export)
- Hook implementation pattern
- Schema validation pattern
- Constants.ts usage for enums and comparisons
- Types.ts definitions for all arguments and objects
- Component composition and layout
- State management via custom hooks
- Theme usage with `useNewTheme()`
- Translation with `translation.useTranslation()`
- Navigation patterns
- Flex layout patterns (row vs column)

---

## 4. PROJECT STRUCTURE

{package_structure}

**Generate code following this structure:**
- `app/features/{feature-name}/views/{screen-name}/index.tsx`
- `app/features/{feature-name}/views/{screen-name}/styles.ts`
- `app/features/{feature-name}/views/{screen-name}/types.ts`
- `app/features/{feature-name}/views/{screen-name}/translations.ts`
- `app/features/{feature-name}/views/{screen-name}/constants.ts` ← **Only if enums/comparisons needed**
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

## 6. API ENDPOINTS (NEW)


{api_endpoints}


**Usage Instructions:**
- Derive API request/response interfaces, constants, and queries from this content.
- Use examples in `api_endpoints` to build mock responses in hooks.
- Always keep URL paths and product/type codes in constants, not hardcoded strings in hooks/views.
- When integrating real APIs, use the same types and constants; only switch implementation from mock to RTK Query + backend.
---

## GENERATION REQUIREMENTS

### Design Analysis

1. Analyze the attached Figma design image carefully.
2. Match structure, layout, spacing, and alignment as closely as possible.
3. **Identify flex-direction** for each container (row vs column based on visual layout).
4. Identify all UI components, layouts, interactions, text content, and styling.
5. Map each visual element to existing custom components.
6. Extract text content, colors, spacing, and typography.
7. Identify form fields that need validation.
8. Note component hierarchy, nesting, and flex behavior.
9. Respect safe-area, scrolling, and keyboard behavior if indicated.
10. Identify if enums/constants are needed for comparisons.
11. Identify correct export pattern for the component.
12. **Identify API endpoints needed** from the provided API endpoints file.

### Code Structure


Generate files in this format:


###FilePath: app/features/{feature}/views/{screen-name}/index.tsx
[View component with screen name export - UI only, uses custom hook, direct component imports]

###FilePath: app/features/{feature}/hooks/use-{screen-name}.ts
[Custom hook - all business logic, state, handlers, API integration]

###FilePath: app/features/{feature}/schemas/{screen-name}-schema.ts
[Yup schema, initial values, types]

###FilePath: app/features/{feature}/views/{screen-name}/styles.ts
[Styles implementation with typed StyleSheet, Theme, and correct flex-direction]

###FilePath: app/features/{feature}/views/{screen-name}/types.ts
[Types/interfaces for props, function arguments, and objects]

###FilePath: app/features/{feature}/views/{screen-name}/translations.ts
[Translation keys with en and ar objects]

###FilePath: app/features/{feature}/views/{screen-name}/constants.ts
[Enums and typed constants - ONLY if comparisons needed]

###FilePath: app/features/{feature}/types/{endpoint-name}.types.ts
[API request/response types derived from api_endpoints]

###FilePath: app/features/{feature}/constants/{endpoint-name}.constants.ts
[API endpoint paths, enums, and config]

###FilePath: app/features/{feature}/queries/use-{endpoint-name}-query.ts
[RTK Query API definitions using the above types/constants]

text


### Implementation Checklist


- [ ] Strict import order (React → Third-party → Components → Theme/utils → Assets → Feature imports → Local)
- [ ] Use path aliases (@app/features, @app/components, @app/assets, @app/constants)
- [ ] Direct component imports (`import {Label, Input} from '@app/components'`)
- [ ] Correct export pattern (named vs default)
- [ ] Component name matches screen name in TitleCase
- [ ] Hooks at feature level
- [ ] Schemas at feature level
- [ ] View-level constants only when comparisons needed
- [ ] All function and object types defined in view-level types.ts
- [ ] Enums for string comparisons (no hardcoded literals)
- [ ] Flex-direction correct
- [ ] View is pure UI (no business logic)
- [ ] All state and handlers in custom hook
- [ ] Formik + Yup used for forms
- [ ] Translations generated with both `en` and `ar`
- [ ] Component IDs follow `ComponentNameFieldName`
- [ ] Translation keys follow `JourneyScreenNameComponentAbbreviationFieldName`
- [ ] Styles typed with ViewStyle/TextStyle/ImageStyle
- [ ] No circular dependencies
- [ ] Figma layout matched
- [ ] **API types present** in `types/{endpoint-name}.types.ts`
- [ ] **API constants present** in `constants/{endpoint-name}.constants.ts`
- [ ] **API queries present** in `queries/use-{endpoint-name}-query.ts`
- [ ] **Mock implementation** in hook using `api_endpoints` examples
- [ ] **Real implementation** ready using RTK Query + `usePostLoginHandler`
- [ ] **All endpoints** referenced via constants, not inline strings


---

## OUTPUT FORMAT


Provide complete, production-ready code organized by file path (including view, hook, schema, styles, types, translations, view-level constants, API types, API constants, and API queries) for the given feature and screen.


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


app/features/{feature}/
├── views/
│ └── {screen-name}/
│ ├── index.tsx # Component exported with screen name
│ ├── styles.ts # StyleSheet definitions
│ ├── types.ts # TypeScript interfaces/types
│ ├── translations.ts # Translation keys (en/ar)
│ └── constants.ts # Enums, typed constants (only if needed)
├── hooks/
│ └── use-{screen-name}.ts # Custom hook (business logic, API calls) - FEATURE LEVEL
├── schemas/
│ └── {screen-name}-schema.ts # Yup validation schema - FEATURE LEVEL
├── queries/ # API queries/mutations - FEATURE LEVEL
│ └── use-{endpoint-name}-query.ts
├── types/ # Feature-level API types
│ └── {endpoint-name}.types.ts
└── constants/ # Feature-level API constants
└── {endpoint-name}.constants.ts

**Path Aliases (from babel.config.js):**
alias: {
'@app': './app',
}

**Import paths in view component:**
// Feature-level imports using PATH ALIASES
import {useScreenName} from '@app/features/{feature}/hooks/use-screen-name';
import {ScreenNameSchema} from '@app/features/{feature}/schemas/screen-name-schema';

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
import {PaymentStatus} from './constants'; // Only if constants.ts exists


**Import paths in hook (for API integration):**
// Feature-level API imports using PATH ALIASES
import {useProfitRateInquiryMutation} from '@app/features/{feature}/queries/use-profit-rate-inquiry-query';
import {
ProfitRateInquiryRequest,
ProfitRateInquiryResponse,
} from '@app/features/{feature}/types/profit-rate-inquiry.types';
import {
API_ENDPOINTS,
ProductType,
} from '@app/features/{feature}/constants/profit-rate-inquiry.constants';

---


## CRITICAL INSTRUCTIONS


### ❌ DO NOT:
- Change existing component structure or component types
- Remove or replace custom component imports
- Create new components or mock implementations
- Use `import * as Components` syntax
- Use `<Components.Label>` component syntax
- Change file paths or file structure (hooks/schemas/queries/types/constants stay at feature level)
- Move hooks, schemas, queries, types, or constants into view folder
- Alter business logic or state management in hooks
- Modify validation schemas or form logic
- Modify TypeScript types unless adding design-specific ones
- Use hardcoded color hex values
- Use hardcoded font families (use theme typography system)
- Change import paths - use path aliases (@app/features/...)
- Use ScaledSheet or string-based spacing ('20@vs', '16@s')
- Use styled-components or CSS-in-JS libraries
- Hardcode comparison values (use enums/constants)
- Change component export names (must match screen name)
- Use incorrect variant capitalization (TitleL, bodyregular)
- Remove or modify API query/types/constants files
- Hardcode API endpoint URLs (use constants)


### ✅ DO:
- Use direct component imports: `import {Label, Input} from '@app/components'`
- Use direct component syntax: `<Label>` not `<Components.Label>`
- Use path aliases: `@app/features/{feature}/hooks/`, `@app/components`
- Use path aliases for API files: `@app/features/{feature}/queries/`, `@app/features/{feature}/types/`
- Enrich styles with precise values from Figma API JSON
- Map Figma colors to existing theme color keys carefully
- Map Figma typography to theme typography variants (titleL, bodyRegularM, etc.)
- Update padding, margin, spacing, borderRadius from Figma data
- Apply font properties via `variant` prop on components (Label, Text)
- Add shadows, borders, opacity values from Figma
- Maintain existing component usage and imports
- Keep hooks at feature level: `app/features/{feature}/hooks/`
- Keep schemas at feature level: `app/features/{feature}/schemas/`
- Keep API queries at feature level: `app/features/{feature}/queries/`
- Keep API types at feature level: `app/features/{feature}/types/`
- Keep API constants at feature level: `app/features/{feature}/constants/`
- Keep file structure: views/{screen}/index.tsx, styles.ts, types.ts, translations.ts
- Use `theme.colors['theme-key']` for all colors
- Use theme typography system via variants
- Preserve proper import patterns (path aliases, direct imports)
- Use standard StyleSheet.create() with number literals
- Export components using screen name (export const ScreenName or export default ScreenName)
- Use enums from constants.ts for comparisons (if applicable)
- Define all function arguments and objects in types.ts
- Use correct variant format (variants.bodyMediumM, not variants.bodymediumm)
- Match flex-direction to visual layout (row for horizontal, column for vertical)
- Preserve existing API integration patterns (mock and real implementations)
- Keep endpoint URLs in constants files, not inline


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


// Figma: {"r": 0.098, "g": 0.027, "b": 0.290, "a": 1} → #19074A → primary-100
backgroundColor: theme.colors['background-04'], // Figma: #19074A → primary-100

// Figma: {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1} → #FFFFFF → neutral-00
color: theme.colors['content-inverted-primary'], // Figma: #FFFFFF → neutral-00

---


## THEME TYPOGRAPHY SYSTEM & VARIANT FORMAT


**CRITICAL:** Variants have specific type case formats that must be followed exactly.


**Variant Format Pattern:** `{style}{Weight}{Size}`
- **Style:** `title` or `body` (lowercase)
- **Weight:** `Semibold`, `Medium`, `Regular` (capitalized) - only for body
- **Size:** `XL`, `L`, `M`, `S`, `XS` (uppercase)


### Available Variants


import {variants} from '@app/components/label/types';

// Title variants (no weight)
variants.titleXL // 28px / 600
variants.titleL // 24px / 800
variants.titleM // 20px / 800
variants.titleS // 18px / 600
variants.titleXS // 16px / 800

// Body variants (with weight)
variants.bodySemiBoldL // 18px / 800
variants.bodyMediumL // 18px / 600
variants.bodyRegularL // 18px / 400
variants.bodySemiBoldM // 16px / 800
variants.bodyMediumM // 16px / 600
variants.bodyRegularM // 16px / 400
variants.bodySemiBoldS // 14px / 800
variants.bodyMediumS // 14px / 600
variants.bodyRegularS // 14px / 400
variants.bodySemiboldXS // 12px / 800 - Note: lowercase 'b' in XS
variants.bodyMediumXS // 12px / 600
variants.bodyRegularXS // 12px / 400

### ⚠️ Special Case: bodySemiboldXS


// Note the lowercase 'b' in 'bold' for XS size only
variants.bodySemiboldXS // ✅ Correct (lowercase 'b')
variants.bodySemiBoldXS // ❌ Wrong


### Figma to Variant Mapping


| Figma Size/Weight | Variant | Usage |
|-------------------|---------|-------|
| 28px / Any | `titleXL` | Large titles |
| 24px / Any | `titleL` | Main titles |
| 20px / Any | `titleM` | Section headers |
| 16px / 800 | `bodySemiBoldM` | Emphasized text |
| 16px / 600 | `bodyMediumM` | Medium body |
| 16px / 400 | `bodyRegularM` | Normal body |
| 14px / 800 | `bodySemiBoldS` | Small bold text |
| 14px / 600 | `bodyMediumS` | Small medium |
| 14px / 400 | `bodyRegularS` | Small text |
| 12px / 800 | `bodySemiboldXS` | Tiny bold (note lowercase) |
| 12px / 600 | `bodyMediumXS` | Tiny medium |
| 12px / 400 | `bodyRegularXS` | Tiny text |


**Weight mapping:** 400=Regular, 500/600=Medium, 700/800=Semibold


### Typography Application


// Method 1: Use variant prop (PREFERRED)
<Label
id="LabelTitle"
text={t('ScreenLblTitle')}
variant={variants.titleL} // Figma: 24px/800 → titleL
style={styles.title} // Only for color, spacing
/>

// Method 2: Override variant if Figma doesn't match exactly
<Label
id="LabelSubtitle"
text={t('ScreenLblSubtitle')}
variant={variants.bodyRegularM}
style={{
...styles.subtitle,
fontSize: 15, // Figma uses 15px, override variant's 16px
}}
/>

// Method 3: In styles.ts - document variant mapping
const styles = StyleSheet.create({
title: {
// Typography via variant={variants.titleL} on component
// Figma: 24px/800/28 → titleL variant
color: theme.colors['content-primary'],
marginBottom: 12,
},
});

---


## FIGMA API JSON ANALYSIS


**From the provided Figma JSON data, extract and apply:**


### 1. **Layout & Spacing**
- `paddingLeft`, `paddingRight`, `paddingTop`, `paddingBottom` → Use number literals
- `itemSpacing` (gap between flex children)
- `layoutMode` (HORIZONTAL → flexDirection: 'row', VERTICAL → flexDirection: 'column')
- `primaryAxisAlignItems` (justifyContent)
- `counterAxisAlignItems` (alignItems)
- `layoutGrow` (flex grow)
- `layoutAlign` (stretch, center, etc.)


**Layout Direction Rules:**
- HORIZONTAL layout → `flexDirection: 'row'`
- VERTICAL layout → `flexDirection: 'column'`
- Match visual structure to flex-direction


### 2. **Typography**
- `fontFamily` → Map to 'figtree' (project standard)
- `fontSize` → Map to variant
- `fontWeight` → Map to variant (400, 600, 800)
- `lineHeightPx` or `lineHeightPercent` → Map to variant
- `letterSpacing` → Apply if specified
- `textAlignHorizontal` → LEFT, CENTER, RIGHT
- `textCase` → UPPER, LOWER, TITLE


**Typography Application Priority:**
1. Match a variant (titleL, bodyRegularM, etc.)
2. If no exact match, choose closest variant + style override
3. Document: `// Figma: 24px/800 → variants.titleL`


### 3. **Colors**
- `fills` array (background colors, gradient fills)
- `strokes` array (border colors)
- `color` (text color)
- Map ALL colors to theme keys - NEVER use raw hex/RGB values


### 4. **Visual Effects**
- `cornerRadius` or `rectangleCornerRadii` (border radius) → Number literal
- `effects` array (shadows, blurs)
  - `type`: DROP_SHADOW, INNER_SHADOW, LAYER_BLUR
  - `color`, `offset`, `radius`, `spread`
- `opacity`
- `strokeWeight` (border width) → Number literal


### 5. **Constraints & Sizing**
- `constraints` (min/max width, height)
- `minWidth`, `maxWidth`, `minHeight`, `maxHeight` → Number literals
- `layoutSizingHorizontal`, `layoutSizingVertical` (FIXED, HUG, FILL)


---


## API INTEGRATION ENRICHMENT (IF APPLICABLE)


**If the current code includes API integration (queries/, types/, constants/ folders), preserve and enrich:**


### API Files Structure (FEATURE LEVEL)


app/features/{feature}/
├── queries/
│ └── use-{endpoint-name}-query.ts # RTK Query endpoints
├── types/
│ └── {endpoint-name}.types.ts # Request/Response types
└── constants/
└── {endpoint-name}.constants.ts # API endpoints, enums


### API Enrichment Rules


1. **DO NOT modify API types** unless Figma reveals new data structures
2. **DO NOT change endpoint paths** in constants (keep placeholders)
3. **DO preserve mock implementations** in hooks
4. **DO preserve real API implementations** using RTK Query + `usePostLoginHandler`
5. **DO maintain path aliases** for API imports: `@app/features/{feature}/queries/`
6. **DO keep API constants** (endpoint URLs, enums) in constants files
7. **DO NOT inline API URLs** - always reference constants


### Example API Hook Pattern (DO NOT BREAK)


// In hooks/use-{screen-name}.ts
import {usePostLoginHandler} from 'app/hooks/post-login-handler';
import {useHeaders} from '@app/features/authentication/hooks';
import {useProfitRateInquiryMutation} from '@app/features/{feature}/queries/use-profit-rate-inquiry-query';
import {
ProfitRateInquiryRequest,
ProfitRateInquiryResponse,
} from '@app/features/{feature}/types/profit-rate-inquiry.types';
import {ProductType} from '@app/features/{feature}/constants/profit-rate-inquiry.constants';

export const useScreenName = () => {
const {getHeaders} = useHeaders();

const {
action: profitRateInquiryAction,
data: profitRateInquiryResponse,
error: profitRateInquiryError,
} = usePostLoginHandler(useProfitRateInquiryMutation);

// Mock implementation (preserved)
const fetchDataMock = async () => {
// Mock logic here
};

// Real implementation (preserved)
const fetchDataReal = () => {
const options = {
headers: getHeaders({screenId: 'ScreenID'}),
request: {
productType: ProductType.RTDEP,
},
};
profitRateInquiryAction(options);
};

useEffect(() => {
if (profitRateInquiryResponse?.isSuccess) {
// Handle success
}
}, [profitRateInquiryResponse, profitRateInquiryError]);

return {
fetchDataMock,
fetchDataReal,
data: profitRateInquiryResponse,
isLoading: !profitRateInquiryResponse && !profitRateInquiryError,
};
};

---


## ENRICHMENT PROCESS


### Step 1: Identify Components in Figma JSON
- Match Figma layer names to React Native components in view
- Find corresponding nodes in JSON by `name`, `id`, or `type`
- Note which file each enrichment applies to (view, styles, types, constants)
- **Do not modify API-related files unless necessary**


### Step 2: Extract Design Properties
- For each matched component, extract all relevant properties
- Note values for spacing (as numbers), colors, typography, effects
- Map typography to variants first
- Identify layout direction (row vs column)
- Focus on styles.ts enrichment
- **Preserve existing API integration patterns**


### Step 3: Map Colors & Typography to Theme
- Convert Figma color values to theme keys
- Map Figma typography to variants (titleL, bodyMediumM, etc.)
- Check for special case: bodySemiboldXS (lowercase 'b')
- Document mapping decisions
- Example: `// Figma: #19074A → primary-100 → background-04`
- Example: `// Figma: 24px/800 → variants.titleL`


### Step 4: Update Styles & Components
- Apply extracted values to StyleSheet in `styles.ts` using number literals
- Update component `variant` props in `index.tsx`
- Set correct flexDirection based on layout (row/column)
- Add style overrides only when variant doesn't match
- Update `getStyles()` with precise measurements
- Do not modify hooks, schemas, or API files unless necessary
- **Preserve all API-related imports and logic**


### Step 5: Validate File Structure & Imports
- Ensure hooks at: `app/features/{feature}/hooks/use-{screen-name}.ts`
- Ensure schemas at: `app/features/{feature}/schemas/{screen-name}-schema.ts`
- Ensure API queries at: `app/features/{feature}/queries/use-{endpoint-name}-query.ts`
- Ensure API types at: `app/features/{feature}/types/{endpoint-name}.types.ts`
- Ensure API constants at: `app/features/{feature}/constants/{endpoint-name}.constants.ts`
- Verify imports use path aliases: `@app/features/{feature}/hooks/`
- Verify direct component imports: `import {Label} from '@app/components'`
- Check component export matches screen name
- Verify correct variant format (lowercase style, capitalized weight, uppercase size)
- Check constants.ts exists only if comparisons are needed
- Verify all function args/objects typed in types.ts
- Verify no ScaledSheet or string-based spacing
- **Verify API imports use path aliases**


---


## OUTPUT FORMAT


Provide the enriched code maintaining the EXACT file structure with proper patterns:


###FilePath: app/features/{feature}/views/{screen-name}/index.tsx
[Component with screen name export - keep existing structure]
[Direct imports: import {Label, Input} from '@app/components']
[Path aliases: import {useScreenName} from '@app/features/{feature}/hooks/use-screen-name']
[Typography via variant props: variant={variants.titleL}]

###FilePath: app/features/{feature}/hooks/use-{screen-name}.ts
[Custom hook - typically unchanged unless new business logic needed]
[FEATURE LEVEL, not in view folder]
[Preserve API integration if present]
[Path aliases for API imports: @app/features/{feature}/queries/]

###FilePath: app/features/{feature}/schemas/{screen-name}-schema.ts
[Validation schema - typically unchanged unless new validation rules]
[FEATURE LEVEL, not in view folder]

###FilePath: app/features/{feature}/views/{screen-name}/styles.ts
[ENRICHED styles with Figma values, theme colors, typography docs]
[Use StyleSheet.create() with number literals]
[Most enrichment happens here]
[Document color mappings: // Figma: #hex → theme-key]
[Document typography: // Figma: fontSize/weight → variant]
[Correct flexDirection based on layout]

###FilePath: app/features/{feature}/views/{screen-name}/types.ts
[Types/interfaces - add design-specific types if needed]
[All function arguments and objects typed here]

###FilePath: app/features/{feature}/views/{screen-name}/translations.ts
[Translation keys - typically unchanged unless new text in Figma]

###FilePath: app/features/{feature}/views/{screen-name}/constants.ts
[ONLY if comparisons/enums needed - otherwise omit]
[Enums for status, types, etc.]

###FilePath: app/features/{feature}/queries/use-{endpoint-name}-query.ts
[API queries - PRESERVE if present, typically unchanged]
[FEATURE LEVEL, not in view folder]

###FilePath: app/features/{feature}/types/{endpoint-name}.types.ts
[API types - PRESERVE if present, typically unchanged]
[FEATURE LEVEL, not in view folder]

###FilePath: app/features/{feature}/constants/{endpoint-name}.constants.ts
[API constants - PRESERVE if present, typically unchanged]
[FEATURE LEVEL, not in view folder]


---


## ENRICHMENT CHECKLIST


For each component/element, verify:
- [ ] Background color mapped to theme key (from Figma `fills`)
- [ ] Text color mapped to theme key (from Figma `color`)
- [ ] Border color mapped to theme key (from Figma `strokes`)
- [ ] Typography mapped to correct variant (titleL, bodyRegularM, bodySemiboldXS, etc.)
- [ ] Variant format correct (lowercase style, capitalized weight, uppercase size)
- [ ] Special case handled: bodySemiboldXS (lowercase 'b')
- [ ] Font size applied via variant or style override
- [ ] Font weight applied via variant
- [ ] Line height applied via variant
- [ ] Padding values as numbers (paddingHorizontal: 16, not '16@s')
- [ ] Margin/spacing as numbers (from Figma `itemSpacing`)
- [ ] Border radius as number (borderRadius: 8, not '8@s')
- [ ] Shadows applied (from Figma `effects`)
- [ ] Opacity applied if < 1
- [ ] Alignment/justification applied
- [ ] FlexDirection correct (row for horizontal, column for vertical)
- [ ] Direct component imports used (no `import * as Components`)
- [ ] Path aliases used (@app/features, not relative paths)
- [ ] Hooks remain at feature level
- [ ] Schemas remain at feature level
- [ ] API queries remain at feature level (if present)
- [ ] API types remain at feature level (if present)
- [ ] API constants remain at feature level (if present)
- [ ] Component syntax is direct (`<Label>` not `<Components.Label>`)
- [ ] Component export name matches screen name
- [ ] Constants.ts created only if comparisons exist
- [ ] All types defined in types.ts
- [ ] API integration patterns preserved (if present)


---


## EXAMPLE ENRICHMENT


**Before (Step-1 Code in index.tsx):**


import * as Components from '@app/components';

<Components.Label
id="LabelTitle"
text={t('ScreenLblTitle')}
style={styles.title}
/>



**After (Enriched):**


import {Label} from '@app/components';
import {variants} from '@app/components/label/types';

<Label
id="LabelTitle"
text={t('ScreenLblTitle')}
variant={variants.titleL} // Figma: 24px/800 → titleL
style={styles.title}
/>


**Before (Step-1 in styles.ts):**


import {ScaledSheet} from 'react-native-size-matters';

return ScaledSheet.create({
title: {
paddingTop: '20@vs',
fontSize: 24,
color: '#19074A',
},
});


**After (Enriched):**


import {StyleSheet, ViewStyle, TextStyle} from 'react-native';
import {Theme} from 'react-core';

interface Styles {
container: ViewStyle;
title: TextStyle;
}

export const getStyles = ({theme}: {theme: Theme}): Styles => {
return StyleSheet.create<Styles>({
container: {
flexDirection: 'column', // Figma: VERTICAL layout
paddingHorizontal: 24, // Figma: paddingLeft + paddingRight
gap: 12, // Figma: itemSpacing
},
title: {
// Typography via variant={variants.titleL} on component
// Figma: 24px/800/28 → titleL variant
color: theme.colors['content-primary'], // Figma: #19074A → primary-100
marginBottom: 12, // Figma: itemSpacing
letterSpacing: -0.5, // Figma: letterSpacing
},
});
};


**API Integration Example (PRESERVE):**


###FilePath: app/features/accounts/hooks/use-profit-rate-screen.ts

// API imports with path aliases (PRESERVE)
import {usePostLoginHandler} from 'app/hooks/post-login-handler';
import {useHeaders} from '@app/features/authentication/hooks';
import {useProfitRateInquiryMutation} from '@app/features/accounts/queries/use-profit-rate-inquiry-query';
import {
ProfitRateInquiryRequest,
ProfitRateInquiryResponse,
} from '@app/features/accounts/types/profit-rate-inquiry.types';
import {ProductType} from '@app/features/accounts/constants/profit-rate-inquiry.constants';

export const useProfitRateScreen = () => {
const {getHeaders} = useHeaders();

const {
action: profitRateInquiryAction,
data: profitRateInquiryResponse,
error: profitRateInquiryError,
} = usePostLoginHandler(useProfitRateInquiryMutation);

// Mock and real implementations preserved
const fetchProfitRatesMock = async () => {
// Mock logic (preserved)
};

const fetchProfitRatesReal = () => {
const options = {
headers: getHeaders({screenId: 'ProfitRateScreen'}),
request: {
productType: ProductType.RTDEP,
},
};
profitRateInquiryAction(options);
};

useEffect(() => {
if (profitRateInquiryResponse?.isSuccess) {
// Handle success
}
}, [profitRateInquiryResponse, profitRateInquiryError]);

return {
fetchProfitRatesMock,
fetchProfitRatesReal,
data: profitRateInquiryResponse,
isLoading: !profitRateInquiryResponse && !profitRateInquiryError,
};
};



---


## SPECIAL NOTES FOR ITERATIVE ENRICHMENT


**Iteration {iteration_number} Focus:**
- This is part {part_number} of {total_parts} of Figma JSON data
- Focus on enriching components/sections in this JSON chunk
- Preserve all enrichments from previous iterations
- Build upon (don't overwrite) previously refined styles
- Always maintain file structure (hooks/schemas/queries/types/constants at feature level)
- Always use path aliases and direct imports
- Always use correct variant format
- Always use number literals for spacing (not strings)
- **Always preserve API integration patterns**


**Handling Conflicts:**
- If current Figma data conflicts with previous iteration, use MORE SPECIFIC value
- Document conflicts in inline comments
- Prioritize visual accuracy to Figma design image
- Never change file locations or import paths
- Never revert to namespace imports or ScaledSheet
- **Never break API integration patterns**


**File Structure & Import Validation:**
After enrichment, verify:
- ✅ Hooks at: `app/features/{feature}/hooks/`
- ✅ Schemas at: `app/features/{feature}/schemas/`
- ✅ API queries at: `app/features/{feature}/queries/` (if present)
- ✅ API types at: `app/features/{feature}/types/` (if present)
- ✅ API constants at: `app/features/{feature}/constants/` (if present)
- ✅ Views at: `app/features/{feature}/views/{screen-name}/`
- ✅ Imports use: `@app/features/{feature}/hooks/`
- ✅ Imports use: `@app/features/{feature}/queries/` (for API)
- ✅ Direct imports: `import {Label} from '@app/components'`
- ✅ Direct syntax: `<Label>` not `<Components.Label>`
- ✅ Variants: lowercase style, capitalized weight, uppercase size
- ✅ Special case: `bodySemiboldXS` (lowercase 'b')
- ✅ StyleSheet.create() with number literals
- ✅ FlexDirection matches layout (row/column)
- ✅ Component export name matches screen name
- ✅ Constants.ts only if comparisons exist
- ✅ All types in types.ts
- ✅ API integration preserved (if present)


---


## WHAT TYPICALLY GETS ENRICHED


**High Frequency:**
- `styles.ts` - Colors, spacing (numbers), shadows, borders, flexDirection
- `index.tsx` - Typography variant props, style adjustments


**Medium Frequency:**
- `types.ts` - New interfaces if Figma reveals complex patterns
- `translations.ts` - New text if Figma has content not in Step-1
- `constants.ts` - Enums if comparisons discovered


**Low Frequency:**
- `hooks/use-{screen-name}.ts` - Only if new business rules (preserve API logic)
- `schemas/{screen-name}-schema.ts` - Only if new validation
- `queries/use-{endpoint-name}-query.ts` - Rarely changed (preserve structure)
- `types/{endpoint-name}.types.ts` - Rarely changed (preserve structure)
- `constants/{endpoint-name}.constants.ts` - Rarely changed (preserve structure)


**Typography Enrichment:**
- Apply via `variant` prop (90% of cases)
- Override in `style` only for non-standard values (10%)
- Document: `// Figma: 24px/800 → variants.titleL`


**Focus Distribution:**
- 60% enrichment on styles.ts
- 30% enrichment on index.tsx (variants)
- 10% enrichment on other files
- 0% on API files (unless new data structures)


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
3. ✅ Use path aliases: `@app/features/{feature}/hooks/`
4. ✅ Use path aliases for API: `@app/features/{feature}/queries/`
5. ✅ Map Figma typography to variants (titleL, bodyRegularM, bodySemiboldXS, etc.)
6. ✅ Use correct variant format (lowercase style, capitalized weight, uppercase size)
7. ✅ Apply typography via `variant` prop on Label/Text
8. ✅ Maintain file structure (hooks/schemas/queries/types/constants at feature level)
9. ✅ Use StyleSheet.create() with number literals (not strings)
10. ✅ Map all colors to theme keys
11. ✅ Set correct flexDirection (row/column) based on layout
12. ✅ Export component with screen name
13. ✅ Keep business logic in hooks unchanged
14. ✅ Preserve API integration patterns (if present)
15. ✅ Document color and typography mappings
16. ✅ Create constants.ts only if comparisons exist
17. ✅ Define all types in types.ts
18. ✅ Keep API constants in constants files (not inline)


Output the complete enriched code ready for the next iteration or final integration.

'''