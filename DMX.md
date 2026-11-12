# DMX / Art-Net

Stand: 2026-11-12. Über Art-Net lassen sich Helligkeit, Planetenfarbe, ein Effekt, die Rotation und der
Moon/Planet-Umschalter steuern. Alles liegt in **einem Block von 9 Kanälen**.

## Einrichten

Im Interface, oben (Parameter am Projekt-COMP `Frequenzfamilie1311`, Seite **DMX**):

| Parameter | Standard | Bedeutung |
|---|---|---|
| **Mode** | Manual | `Manual (this interface)`: die Regler im Interface gelten. `DMX (Art-Net)`: die Kanäle unten gelten. |
| **Net** | 0 | Art-Net Net (0-127) |
| **Subnet** | 0 | Art-Net Subnet (0-15) |
| **Universe** | 0 | Art-Net Universe (0-15) |
| **Start Channel** | 1 | Erster Kanal des 9er-Blocks (1-504) |
| **Network Adapter** | leer = alle | Auf welcher Netzwerkkarte (IP dieses Rechners) Art-Net gehört wird. Bei Problemen die Karte wählen, die im Netz des Pults liegt. |
| **Listening On** | (nur Anzeige) | Aktuelle Adresse, z.B. `Net 0 / Sub 0 / Uni 0 (Art-Net universe 0) channels 1-9` |
| **Channel Values** | (nur Anzeige) | Wie viele der 9 Kanäle gerade einen Wert über 0 haben. 0 = nichts (oder nur Nullen) angekommen. Zuletzt empfangene Werte bleiben stehen. |

Art-Net kommt per UDP auf Port 6454 an. Das Pult (oder MadMapper) muss im selben Netz senden.

Ein Schalter für alles: bei `DMX (Art-Net)` ignorieren Farbwähler, Output-Menü und Effekt-Regler im Interface
(sie ändern nichts, auch wenn man sie bewegt). Die Regler zeigen dann **nicht** die DMX-Werte an.

**Wichtig:** Kommt in DMX-Modus kein Signal an, stehen alle Kanäle auf 0 (Planet schwarz, Mond on air,
alle Effekte aus). Zum Zurückholen den Mode wieder auf `Manual` stellen.

## Kanalbelegung

Kanal = Start Channel + Offset. In der Tabelle gilt Start Channel = 1. Alle Werte 0-255.

| Kanal | Funktion | Werte |
|---|---|---|
| 1 | Dimmer | 0 = dunkel, 255 = volle Helligkeit |
| 2 | Planet Rot | 0-255 |
| 3 | Planet Grün | 0-255 |
| 4 | Planet Blau | 0-255 |
| 5 | Effect Select | 8 Stufen à 32 Werte (siehe unten) |
| 6 | Effect Size | 0-255 = 0-100 %, Stärke bzw. Größe des gewählten Effekts |
| 7 | Effect Speed | 0-255 = 0-100 %, Tempo oder zweiter Parameter des gewählten Effekts |
| 8 | Rotation Speed | 0 = steht, ca. 57 = bisheriges Tempo, 255 = schnell (quadratisch, unten feiner) |
| 9 | **Output** | 0-127 = Mond, 128-255 = Planet |

Effect Select, immer nur ein Effekt aktiv:

| Wert | Effekt | Size | Speed |
|---|---|---|---|
| 0-31 | aus | | |
| 32-63 | Pulse | Zoom-Stärke | Beat-Rate (schnell = kürzere Teilung) |
| 64-95 | Glitch | Stärke | Tempo |
| 96-127 | Chroma | Stärke | |
| 128-159 | Bloom | Größe | Stärke |
| 160-191 | Flash | Stärke | Beat-Rate |
| 192-223 | Dither | Punktgröße | Farbstufen |
| 224-255 | ASCII | Zeichengröße | |

Pulse, Flash und Glitch-auf-dem-Beat reagieren auf den Beat (Ableton Link, siehe unten).

Output: Kanal 9 auf 0 schaltet auf den Mond, auf 255 auf den Planeten. Der Wechsel ist eine Überblendung
(Parameter **Fade Time** am Projekt-COMP, Seite Show, Standard 1,5 s, 0 = harter Schnitt). Währenddessen
rendern beide, danach pausiert der nicht sichtbare (kein Rendering). Es gibt nur einen Syphon-Output
(`Frequenzfamilie`); er bleibt immer an, nur das Bild darin wechselt.

Bei anderem Start Channel verschiebt sich der ganze Block (Start Channel 10: Dimmer = 10, Output = 18).

## MadMapper

Ein Fixture mit 9 Kanälen vom Typ **Slider** (8 Bit), Universe 0, Startadresse 1, Art-Net einschalten
(*Preferences > Project > DMX*). R/G/B/L/W-Kanäle nicht verwenden, die nehmen ihren Wert aus dem Bild.

## Beat (Ableton Link)

Der Beat kommt per **Ableton Link** (Seite **Beat** im Interface, rechts unten). `Ableton Link` ist standardmäßig
an: TouchDesigner tritt der Link-Session im Netz bei und folgt Tempo und Beat-Position. Läuft kein anderer
Link-Teilnehmer (Ableton Live, Resolume usw.), läuft die Uhr allein mit 120 BPM (Anzeige `running alone`).
Die Zeile **Link Status** zeigt, ob und mit wie vielen Teilnehmern verbunden wird und das Tempo.

## Hinweise

- Die Planetenfarbe wirkt nur auf den Planeten. Der Mond bleibt grau.
- Die Effekte gelten für beide (Mond und Planet) und stehen vor dem Syphon-Ausgang.
- Alle Effekte sind auf den Kreis (Projektionsfläche) beschränkt.
- Schaltet das Pult den Output um, reagiert auch die Anzeige im Interface (`On Air (effective)`).

## Test ohne Pult

Ein Art-Net-Paket (Port 6454, Net 0 / Subnet 0 / Universe 0) mit Kanal 1-4 = 255 / 255 / 40 / 0 stellt den
Planeten rot. Die empfangenen Rohwerte (0-255) zeigt der CHOP `dmx/dmxin_all` (`c1` ... `c512`), die daraus
berechneten wirksamen Werte `dmx/null_control` (Namen: `r`, `g`, `b`, `output`, `glitch`, ...).

## Wo es technisch liegt

`/Frequenzfamilie1311/dmx`: `dmxin_all` (Empfang) -> `script_dmx` (Kanäle -> Werte im jeweiligen Bereich,
Code in `script_dmx_callbacks`) und `constant_manual` (Werte aus den Interface-Parametern) -> `switch_source`
(Mode) -> `null_control` (die wirksamen Werte). Planet (`planet/select_colour`), Effekte (`fx/glsl_*`) und
der Output-Schalter (`Onair` am Projekt-COMP) lesen nur noch `null_control`. Die Überblendung Mond/Planet
läuft in `fx` (`constant_target` -> `lag_mix` -> `null_mix`, `chopexec_mix`).
