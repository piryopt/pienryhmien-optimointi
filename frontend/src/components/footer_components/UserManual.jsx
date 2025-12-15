import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import { Link } from "react-router-dom";
import "../../static/css/dark.css";

const langToFile = {
  fi: "/content/user-manual-fi.md",
  en: "/content/user-manual-en.md",
  sv: "/content/user-manual-sv.md"
};

const UserManual = () => {
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
        rehypePlugins={[rehypeRaw]}
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

export default UserManual;
