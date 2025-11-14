import { baseUrl } from "../utils/constants";

const fetchDebugFlag = async () => {
  const response = await fetch(`${baseUrl}/config`, {
    credentials: "include"
  });
  const data = await response.json();
  return data.debug;
};

export default {
  fetchDebugFlag: fetchDebugFlag
};
