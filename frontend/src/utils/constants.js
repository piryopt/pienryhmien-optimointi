const STAGE = import.meta.env.VITE_STAGE || "development";

const HOSTS = {
  development: "http://localhost:5001",
  staging: "https://jakaja-test.it.helsinki.fi",
  production: "https://jakaja.it.helsinki.fi",
  testing: "http://web-test:5000",
  ci: "http://localhost:5000"
};

const apiHost = HOSTS[STAGE] || HOSTS.development;

export const baseUrl = `${apiHost}/api`;
export const imagesBaseUrl = `${apiHost}/static/images`;

export const languages = {
  fi: {
    logo: `${imagesBaseUrl}/fin.svg`,
    alt: "Finnish flag"
  },
  en: {
    logo: `${imagesBaseUrl}/eng.svg`,
    alt: "British flag"
  },
  sv: {
    logo: `${imagesBaseUrl}/swe.svg`,
    alt: "Swedish flag"
  }
};
