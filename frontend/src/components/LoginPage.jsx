import { useState } from "react";
import axios from "axios";
import csrfService from "../services/csrf";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post("http://localhost:5001/auth/login", {
        "username": username,
        "password": password
      }, {
        headers: {
          "X-CSRFToken": csrfToken
        },
      withCredentials: true
      });
    console.log(response)
  };

  return (
    <div>
      <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <div>
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit">Login</button>
        </form>
    </div>
  );
}

export default Login;