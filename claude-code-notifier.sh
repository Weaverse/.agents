#!/bin/bash

#==============================================================================
# Claude Code Notification Hook Script
# This script displays system notifications when Claude Code triggers hooks
#==============================================================================

# Read JSON input from stdin
input=$(cat)

# Extract message and event from JSON input
message=$(echo "$input" | jq -r '.message // "Claude Code Notification"')
hook_event=$(echo "$input" | jq -r '.hook_event_name // "Unknown"')

# Fallback if jq is not available
if [ $? -ne 0 ] || [ "$message" = "null" ]; then
  message="Claude Code Notification"
fi

#==============================================================================
# Customize message based on event type
#==============================================================================
case "$hook_event" in
  "SessionStart")
    message="Session started 🚀"
    ;;
  "SessionEnd")
    message="Session completed ✅"
    ;;
  "Stop")
    message="Response finished 🏁"
    ;;
  "Notification")
    # Keep the original message from Claude
    ;;
  *)
    message="$hook_event: $message"
    ;;
esac

#==============================================================================
# Detect operating system and show notification accordingly
#==============================================================================
case "$(uname -s)" in
  Darwin*)
    # macOS - use terminal-notifier
    terminal-notifier -title "Claude Code" -message "$message" -sound default
    ;;
    
  Linux*)
    # Linux - use notify-send
    if command -v notify-send >/dev/null 2>&1; then
      notify-send "Claude Code" "$message" -i dialog-information
    else
      echo "notify-send not found. Install libnotify-bin package."
      echo "Claude Code: $message"
    fi
    ;;
    
  CYGWIN*|MINGW*|MSYS*)
    # Windows - use PowerShell toast notification
    powershell.exe -Command "
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null;
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null;
    \$template = @'
    <toast>
        <visual>
            <binding template=\"ToastGeneric\">
                <text>Claude Code</text>
                <text>$message</text>
            </binding>
        </visual>
    </toast>
'@;
    \$xml = New-Object Windows.Data.Xml.Dom.XmlDocument;
    \$xml.LoadXml(\$template);
    \$toast = [Windows.UI.Notifications.ToastNotification]::new(\$xml);
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show(\$toast);"
    ;;
    
  *)
    # Fallback - just echo to terminal
    echo "Claude Code Notification: $message"
    ;;
esac
