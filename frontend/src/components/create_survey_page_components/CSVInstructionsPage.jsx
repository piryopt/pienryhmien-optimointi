import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import MarkdownRenderer from "../MarkdownRenderer";

const langToFile = {
  fi: "/content/csv-instructions-fi.md",
  en: "/content/csv-instructions-en.md",
  sv: "/content/csv-instructions-sv.md"
};

const CSVInstructionsPage = () => {
  const { i18n } = useTranslation();
  const [markdown, setMarkdown] = useState("");

  useEffect(() => {
    const file = langToFile[i18n.language] || langToFile.fi;
    fetch(file)
      .then((res) => res.text())
      .then(setMarkdown);
  }, [i18n.language]);

  return (
    <div className="container">
      <MarkdownRenderer content={markdown} />
    </div>
  );
};

export default CSVInstructionsPage;
