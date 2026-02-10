# rofi-prompt

A rofi integration for AI agent prompts with a customizable result display window.

## Features

- **Multiple AI Agents**: Supports OpenCode and Claude Code
- **Minimal UI**: Clean, dark-themed interface with transparent close button

## Example hyprland setup

1. Clone this repository to your rofi scripts directory:
   ```bash
   cd ~/.config/rofi/scripts/
   git clone https://github.com/joao-paulo-santos/rofi-prompt.git
   ```

2. Add the following to your Hyprland config:
   ```bash
   $promptMenu = rofi -show prompt -modi "prompt:~/.config/rofi/scripts/rofi-prompt/rofi-prompt.js" -no-history -no-sort
   ```

3. Add window rules to Hyprland config:
   ```bash
   windowrulev2 = float,class:^(prompt-result)$
   windowrulev2 = center,class:^(prompt-result)$
   windowrulev2 = keep_above,class:^(prompt-result)$
   windowrulev2 = pin,class:^(prompt-result)$
   windowrulev2 = noblur,class:^(prompt-result)$
   windowrulev2 = nodim,class:^(prompt-result)$
   ```

4. Bind the menu to a key in your keybind config:
    ```bash
    bind = $mainMod $mod3, Space, exec, $promptMenu
    ```

## Configuration

### Switching AI Agents

Set the `PROMPT_AGENT` environment variable before launching the script:

- **OpenCode** (default):
  ```bash
  PROMPT_AGENT=opencode
  ```

- **Claude Code**:
  ```bash
  PROMPT_AGENT=claude
  ```

### Adding New Agents

Edit `rofi-prompt.js` and add your agent to the `AGENTS` object:

```javascript
const AGENTS = {
  your_agent: {
    command: 'your-command -p',
    label: 'Your Agent'
  }
};
```

## Dependencies

- Node.js (for rofi-prompt.js)
- Python 3 with PyGObject (for show_prompt_result.py)
- rofi
- Your AI agent of choice (OpenCode, Claude Code, etc.)

## Usage

1. Launch the rofi prompt menu
2. Type your question or command
3. Press Enter
4. View results in the popup window when they are ready

The window automatically adjusts its size based on the content length and line count.
