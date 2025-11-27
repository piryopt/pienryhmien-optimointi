// eslint.config.js
import js from "@eslint/js";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import vitest from "@vitest/eslint-plugin";
import globals from "globals";

export default [
  // Base JavaScript config
  js.configs.recommended,

  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser
      },
      parserOptions: {
        ecmaFeatures: {
          jsx: true
        }
      }
    },
    plugins: {
      react,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh
    },
    settings: {
      react: {
        version: "detect"
      }
    },
    rules: {
      ...react.configs.recommended.rules,
      ...react.configs["jsx-runtime"].rules,
      ...reactHooks.configs.recommended.rules,

      // React Refresh (Vite fast refresh)
      "react-refresh/only-export-components": [
        "warn",
        { allowConstantExport: true }
      ],

      "react/prop-types": "off",
      "react/self-closing-comp": "warn",
      "no-console": "warn"
    }
  },

  // Vitest-specific config
  {
    files: ["**/*.test.{js,jsx}"],
    plugins: {
      vitest
    },
    languageOptions: {
      globals: {
        ...globals.vitest
      }
    },
    rules: {
      ...vitest.configs.recommended.rules
    }
  }
];
