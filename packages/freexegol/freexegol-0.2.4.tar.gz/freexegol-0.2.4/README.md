# Freexegol


**⚠️ THIS PROJECT IS STILL UNDER DEVELOPMENT ⚠️**


![FreeXegol Presentation](assets/freexegol.png)

---

## Introduction

**Freexegol** is the free, open-source, and lifetime alternative to the Exegol project  
(actually, it's a crappy project but it's free for commercial use!)

---

### Disclaimer

This project is **not** intended to overshadow the amazing [Exegol project](https://exegol.com), which we greatly appreciate and recommend.  
However, since Exegol is no longer free for commercial use, **Freexegol** exists only to provide a minimalist, usable, and truly free alternative for commercial contexts.

---

## Features

- **Strictly necessary functionalities only:**
  - A ready-to-go custom Docker container
  - Recording of commands and their output using [asciinema](https://asciinema.org)
  - A Python wrapper for basic container management

---

## Installation

```bash
pip install freexegol
```

---

## How to use

- **`freexegol build`**: Build the local Dockerfile in the `image` folder.
- **`freexegol install`**: Install the pre-built image from the Docker registry.
- **`freexegol start <container_name>`**: Create or start a container.
- **`freexegol stop <container_name>`**: Stop an existing container.
- **`freexegol inspect <container_name>`**: Display information about an existing container.
- **`freexegol remove <container_name>`**: Remove a container and its folders.

---

## License & Philosophy

Freexegol will **always** be free and available for commercial use.  
No vendor lock-in, no subscription, no hidden costs—free, forever.

---

This project is designed for a Windows x64 hosting Docker Desktop with WSL2 integration.

Feel free to submit issues or contribute!
