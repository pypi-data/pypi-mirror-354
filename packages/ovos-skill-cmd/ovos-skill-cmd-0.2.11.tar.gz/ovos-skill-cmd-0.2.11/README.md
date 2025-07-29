# Commands Skill

A simple OVOS skill for running shell scripts and other commands. The commands execute quietly without requiring confirmation from OVOS.

## Features

- Run shell scripts or commands by speaking human-readable phrases.
- Configure aliases for easy-to-remember commands.
- Optionally run commands under a specific user's privileges.

## Usage

Trigger commands using phrases like:

- **"Hey Mycroft, launch command echo TEST"**
- **"Hey Mycroft, run script generate report"**

## Configuration

The skill can be configured to map spoken phrases to scripts or commands in the `settings.json` file. For example:

```json
{
  "alias": {
    "generate report": "/home/forslund/scripts/generate_report.sh"
  }
}
```

### Example:
- User says: **"Run script generate report"**  
- The skill executes: `/home/forslund/scripts/generate_report.sh`

### Additional Settings:

- **`user`** *(optional)*: Specify a username to run commands under their privileges. Example:
  ```json
  {
    "user": "ovos"
  }
  ```

- **`shell`** *(optional)*: Determines whether commands are executed via a shell. Defaults to `true`. Example:
  ```json
  {
    "shell": false
  }
  ```

### Full Configuration Example:
```json
{
  "user": "ovos",
  "alias": {
    "generate report": "/home/forslund/scripts/generate_report.sh",
    "update system": "sudo apt update && sudo apt upgrade -y",
    "reboot device": "sudo reboot"
  },
  "shell": true
}
```

## Security Notes

1. **Shell Commands**: 
   - By default, commands are executed via the shell, which allows complex operations but may expose security risks. If your commands don’t require shell features, set `shell` to `false`.

2. **User Permissions**: 
   - Commands can run under a specific user by configuring the `user` field. Ensure that the user has appropriate permissions to execute the commands.

3. **Validation**:
   - Avoid configuring dangerous commands like `rm -rf` without additional safeguards.


## Note for using the skill in Docker containers:

All commands run exclusively within the Docker container. If the commands/scripts are also supposed to have an effect outside the container, additional solutions are required. Here is an example for steering kodi (outsight the container) with ovos-skill-cmd:

```json
{
    "alias": {
        "kodi restart": "echo \"systemctl restart kodi\" > /home/ovos/.config/mycroft/joespipe",
        "kodi mute": "echo \"kodi-send --action=\\\"Mute\\\"\" > /home/ovos/.config/mycroft/joespipe",
        "kodi unmute": "echo \"kodi-send --action=\\\"Mute\\\"\"  > /home/ovos/.config/mycroft/joespipe",
        "kodi louder": "echo \"kodi-send --action=\\\"VolumeUp\\\"\" > /home/ovos/.config/mycroft/joespipe",
        "kodi lower": "echo \"kodi-send --action=\\\"VolumeDown\\\"\" > /home/ovos/.config/mycroft/joespipe",
        "kodi pause": "echo \"kodi-send --action=\\\"PlayerControl(Play)\\\"\" > /home/ovos/.config/mycroft/joespipe",
        "kodi resume": "echo \"kodi-send --action=\\\"PlayerControl(Play)\\\"\" > /home/ovos/.config/mycroft/joespipe",
        "kodi stop": "echo \"kodi-send --action=\\\"PlayerControl(Stop)\\\"\" > /home/ovos/.config/mycroft/joespipe"
    },
    "shell": true,
    "__mycroft_skill_firstrun": false
}
```

"/home/ovos/.config/mycroft/joespipe" is a named pipe placed in the shared volume of the ovos config folder. Outside of the container is a mini script watching for commands in the pipe:

```json
#!/bin/bash
while true; do eval "$(cat /storage/ovos/config/joespipe)"; done
```
A description for the named pipe solution you can find [here](https://stackoverflow.com/questions/32163955/how-to-run-shell-script-on-host-from-docker-container)
