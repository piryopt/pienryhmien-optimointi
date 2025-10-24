import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

const langToFile = {
  fi: "/content/faq-fi.md",
  en: "/content/faq-en.md",
  sv: "/content/faq-sv.md"
};

const FAQ = () => {
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
      <ReactMarkdown>{markdown}</ReactMarkdown>
    </div>
  );
};

export default FAQ;
