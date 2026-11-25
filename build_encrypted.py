"""Krypterar cv-source.html till en lösenordsskyddad index.html med AES-256-GCM."""

import argparse
import base64
import getpass
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 310_000

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Max Andersen Frisk — CV &amp; Portfölj</title>
  <meta name="description" content="Lösenordsskyddat CV och portfölj för Max Andersen Frisk.">
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <style>
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    :root {{
      --bg: #f8fafc;
      --card: #ffffff;
      --text: #0f172a;
      --muted: #475569;
      --border: #e2e8f0;
      --accent: #2563eb;
      --accent-hover: #1d4ed8;
      --error: #dc2626;
      --error-bg: #fef2f2;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #0f172a;
        --card: #1e293b;
        --text: #f1f5f9;
        --muted: #94a3b8;
        --border: #334155;
        --accent: #3b82f6;
        --accent-hover: #2563eb;
        --error: #f87171;
        --error-bg: rgba(220, 38, 38, 0.12);
      }}
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
      line-height: 1.5;
    }}
    .lock-card {{
      width: 100%;
      max-width: 420px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 2.25rem 2rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
    }}
    .lock-icon {{
      width: 44px;
      height: 44px;
      border-radius: 12px;
      background: rgba(37, 99, 235, 0.1);
      color: var(--accent);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 1.25rem;
    }}
    h1 {{
      font-size: 1.35rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 0.4rem;
    }}
    .subtitle {{
      font-size: 0.94rem;
      color: var(--muted);
      margin-bottom: 1.5rem;
    }}
    label {{
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 0.45rem;
    }}
    .input-row {{
      position: relative;
      margin-bottom: 1rem;
    }}
    input[type="password"],
    input[type="text"] {{
      width: 100%;
      padding: 0.75rem 2.75rem 0.75rem 0.9rem;
      font-size: 1rem;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: var(--bg);
      color: var(--text);
      outline: none;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    }}
    .toggle-pw {{
      position: absolute;
      right: 0.65rem;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--muted);
      cursor: pointer;
      padding: 0.25rem;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .toggle-pw:hover {{
      color: var(--text);
    }}
    .submit-btn {{
      width: 100%;
      padding: 0.8rem 1rem;
      font-size: 0.98rem;
      font-weight: 600;
      color: #ffffff;
      background: var(--accent);
      border: none;
      border-radius: 10px;
      cursor: pointer;
      transition: background-color 0.15s ease, opacity 0.15s ease;
    }}
    .submit-btn:hover {{
      background: var(--accent-hover);
    }}
    .submit-btn:disabled {{
      opacity: 0.65;
      cursor: not-allowed;
    }}
    .error-msg {{
      display: none;
      margin-top: 0.9rem;
      padding: 0.65rem 0.85rem;
      border-radius: 8px;
      background: var(--error-bg);
      color: var(--error);
      font-size: 0.88rem;
      font-weight: 500;
    }}
    .error-msg.visible {{
      display: block;
    }}
  </style>
</head>
<body>
  <main class="lock-card">
    <div class="lock-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
      </svg>
    </div>
    <h1>Max Andersen Frisk</h1>
    <p class="subtitle">Detta CV är lösenordsskyddat. Ange koden du fått för att visa innehållet.</p>

    <form id="unlock-form" autocomplete="off">
      <label for="pw-input">Lösenord</label>
      <div class="input-row">
        <input id="pw-input" type="password" placeholder="Ange lösenord..." required autofocus>
        <button type="button" id="toggle-pw" class="toggle-pw" aria-label="Visa lösenord">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </button>
      </div>
      <button type="submit" id="submit-btn" class="submit-btn">Öppna CV</button>
      <p id="error-msg" class="error-msg" role="alert">Fel lösenord. Kontrollera koden och försök igen.</p>
    </form>
  </main>

  <script>
    (function () {{
      const SALT_B64 = "{salt_b64}";
      const IV_B64 = "{iv_b64}";
      const CIPHER_B64 = "{cipher_b64}";
      const ITERATIONS = {iterations};

      function b64ToBytes(b64) {{
        const bin = atob(b64);
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) {{
          bytes[i] = bin.charCodeAt(i);
        }}
        return bytes;
      }}

      const form = document.getElementById("unlock-form");
      const pwInput = document.getElementById("pw-input");
      const toggleBtn = document.getElementById("toggle-pw");
      const submitBtn = document.getElementById("submit-btn");
      const errorMsg = document.getElementById("error-msg");

      toggleBtn.addEventListener("click", () => {{
        const isPw = pwInput.type === "password";
        pwInput.type = isPw ? "text" : "password";
        toggleBtn.setAttribute("aria-label", isPw ? "Dölj lösenord" : "Visa lösenord");
      }});

      form.addEventListener("submit", async (e) => {{
        e.preventDefault();
        errorMsg.classList.remove("visible");
        submitBtn.disabled = true;
        submitBtn.textContent = "Låser upp...";

        try {{
          const enc = new TextEncoder();
          const keyMaterial = await window.crypto.subtle.importKey(
            "raw",
            enc.encode(pwInput.value),
            "PBKDF2",
            false,
            ["deriveKey"]
          );

          const key = await window.crypto.subtle.deriveKey(
            {{
              name: "PBKDF2",
              salt: b64ToBytes(SALT_B64),
              iterations: ITERATIONS,
              hash: "SHA-256"
            }},
            keyMaterial,
            {{ name: "AES-GCM", length: 256 }},
            false,
            ["decrypt"]
          );

          const decryptedBuffer = await window.crypto.subtle.decrypt(
            {{ name: "AES-GCM", iv: b64ToBytes(IV_B64) }},
            key,
            b64ToBytes(CIPHER_B64)
          );

          const html = new TextDecoder().decode(decryptedBuffer);
          document.open();
          document.write(html);
          document.close();
        }} catch (_err) {{
          errorMsg.classList.add("visible");
          submitBtn.disabled = false;
          submitBtn.textContent = "Öppna CV";
          pwInput.select();
        }}
      }});
    }})();
  </script>
</body>
</html>
"""


def encrypt_cv(source_path: Path, output_path: Path, password: str) -> None:
    """Krypterar källfilen med PBKDF2-HMAC-SHA256 och AES-256-GCM."""
    plaintext = source_path.read_text(encoding="utf-8").encode("utf-8")
    salt = os.urandom(16)
    iv = os.urandom(12)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = kdf.derive(password.encode("utf-8"))
    ciphertext = AESGCM(key).encrypt(iv, plaintext, None)

    rendered = HTML_TEMPLATE.format(
        salt_b64=base64.b64encode(salt).decode("ascii"),
        iv_b64=base64.b64encode(iv).decode("ascii"),
        cipher_b64=base64.b64encode(ciphertext).decode("ascii"),
        iterations=ITERATIONS,
    )
    output_path.write_text(rendered, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Kryptera cv-source.html till index.html")
    parser.add_argument("--password", help="Lösenord för att kryptera CV:t")
    args = parser.parse_args()

    password = args.password or getpass.getpass("Ange lösenord för kryptering: ")
    if not password:
        raise SystemExit("Lösenordet kan inte vara tomt.")

    root = Path(__file__).resolve().parent
    source_path = root / "cv-source.html"
    output_path = root / "index.html"

    if not source_path.exists():
        raise SystemExit(f"Hittar inte {source_path}")

    encrypt_cv(source_path, output_path, password)
    print(f"Krypterade {source_path.name} -> {output_path.name}")


if __name__ == "__main__":
    main()
