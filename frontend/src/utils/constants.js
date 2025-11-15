const STAGE = import.meta.env.VITE_STAGE || "dev";

const HOSTS = {
  dev: "http://localhost:5001",
  staging: "https://jakaja-test.it.helsinki.fi",
  production: "https://jakaja.it.helsinki.fi"
};

const apiHost = HOSTS[STAGE] || HOSTS.dev;

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
