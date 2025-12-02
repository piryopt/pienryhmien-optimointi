import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Link } from "react-router-dom";

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
      <ReactMarkdown
        components={{
          a: ({ href, children, ...props }) =>
            href && href.startsWith("/") ? (
              <Link to={href} {...props}>
                {children}
              </Link>
            ) : (
              <a href={href} {...props}>
                {children}
              </a>
            )
        }}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
};

export default FAQ;
