# YouTube AI Agent

Ein schlanker AI-Agent, der aus YouTube-Video-Transkripten strukturierte Markdown-Notizen mit OpenAI generiert.

## 🚀 Features

- ✅ Automatische Transkript-Extraktion von YouTube-Videos
- ✅ OpenAI-basierte Inhaltsanalyse und Zusammenfassung  
- ✅ Strukturierte Markdown-Ausgabe (TL;DR, Kernaussagen, Gliederung)
- ✅ Unterstützung für deutsche und englische Videos
- ✅ Zeitstempel-basierte Zitate (optional)
- ✅ CLI-Interface mit ausführlicher Hilfe
- ✅ Zusätzliche Sektionen (Glossar, offene Fragen, nächste Schritte)
- ✅ Konfigurierbare Ausgabe-Verzeichnisse und AI-Modelle

## 📦 Installation

### Mit UV (empfohlen)
```bash
# Repository klonen oder manuell erstellen
mkdir youtube-ai-agent && cd youtube-ai-agent

# UV installieren (falls nicht vorhanden)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Projekt setup
uv init --name youtube-ai-agent --python 3.12
# ... [Code-Dateien erstellen wie in der Anleitung] ...

# Dependencies installieren
uv sync
```

## ⚙️ Konfiguration

### API Key einrichten
```bash
# Setup-Assistent starten
youtube-ai-agent setup

# Oder manuell .env erstellen
cp .env.example .env
```

Trage deinen OpenAI API Key in `.env` ein:
```env
# AI Provider Configuration
OPENAI_API_KEY=your_openai_api_key_here
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini/

# Output Configuration
OUTPUT_DIR=output

# Processing Configuration
MAX_TRANSCRIPT_LENGTH=10000
```

## 🎯 Verwendung

### Basis-Commands

```bash
# Hilfe anzeigen
youtube-ai-agent --help

# Setup und Konfiguration prüfen
youtube-ai-agent setup

# Video verarbeiten (einfach)
youtube-ai-agent process-video "https://www.youtube.com/watch?v=VIDEO_ID"

# Video verarbeiten (mit Optionen)
youtube-ai-agent process-video [OPTIONS] YOUTUBE_URL
```

### Verfügbare Commands

#### `setup`
Prüft die Konfiguration und API Keys:
```bash
youtube-ai-agent setup
```

#### `process-video`
Hauptfunktion zum Verarbeiten von Videos:
```bash
youtube-ai-agent process-video [OPTIONS] YOUTUBE_URL
```

**Optionen:**
- `-o, --output-dir TEXT`: Ausgabe-Verzeichnis (Standard: `output`)
- `-m, --model TEXT`: AI-Modell
- `-v, --verbose`: Ausführliche Ausgabe
- `--help`: Hilfe für diesen Command

### Beispiele

```bash
# Deutsches Video verarbeiten
youtube-ai-agent process-video "https://www.youtube.com/watch?v=jNQXAC9IVRw" --verbose

# Mit benutzerdefiniertem Ausgabe-Verzeichnis
youtube-ai-agent process-video \
  --output-dir ./my-notes \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Mit anderem OPENAI-Modell
youtube-ai-agent process-video \
  --model gpt-4o-mini \
  --verbose \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Kurze Ausgabe ohne Details
youtube-ai-agent process-video "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Unterstützte Video-URLs
```bash
# Standard YouTube URLs
https://www.youtube.com/watch?v=VIDEO_ID

# Kurze YouTube URLs  
https://youtu.be/VIDEO_ID

# Mit Zeitstempel (wird ignoriert)
https://www.youtube.com/watch?v=VIDEO_ID&t=123s
```

## 📋 Ausgabe-Format

Das Tool generiert strukturierte Markdown-Dateien mit folgendem Format:

```markdown
# Video-Titel
- Quelle: https://www.youtube.com/watch?v=VIDEO_ID

## TL;DR
- Kurze Zusammenfassung Punkt 1
- Kurze Zusammenfassung Punkt 2
- Kurze Zusammenfassung Punkt 3

## Kernaussagen
- Wichtige Erkenntnis 1
- Wichtige Erkenntnis 2
- Wichtige Erkenntnis 3

## Struktur / Outline
1. Einführung
2. Hauptteil
3. Schlussfolgerungen

## Wichtige Zitate
- "Wichtiges Zitat aus dem Video" (12:34)

## Glossar
- Fachbegriff: Erklärung des Begriffs

## Offene Fragen
- Frage, die sich aus dem Video ergibt
```

### Dateinamen
Dateien werden automatisch benannt basierend auf dem Video-Titel:
- `ki-in-der-medizin-revolutionaere-ansaetze.md`
- `python-tutorial-fuer-anfaenger-grundlagen.md`

## 🏗️ Architektur

```
┌─────────────────┐    ┌──────────────────┐      ┌─────────────────┐
    YouTube URL    ───▶  Transcript API    ───▶      AI Service     
└─────────────────┘    └──────────────────┘      └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐              │
   Markdown File   ◀───    File Output     ◀────────────┘
└─────────────────┘    └──────────────────┘
```


## 📝 Limitierungen

- Funktioniert nur mit öffentlichen YouTube-Videos
- Benötigt verfügbare Untertitel/Transkripte
- Maximale Transkript-Länge: 15.000 Zeichen
- Abhängig von OpenAI API Rate Limits
- Qualität abhängig vom gewählten OpenAI-Modell
