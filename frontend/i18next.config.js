import { defineConfig } from "i18next-cli";

/** @type {import('i18next-cli').I18nextToolkitConfig} */
export default defineConfig({
  locales: ["en", "fi", "sv"],
  extract: {
    input: "src/**/*.{js,jsx,ts,tsx}",
    output: "public/locales/{{language}}/{{namespace}}.json",
    primaryLanguage: "fi",
    secondaryLanguages: ["en", "sv"],
  },
});

