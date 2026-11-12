# DMX / Art-Net

Stand: 2026-11-12. Über Art-Net lassen sich die Planetenfarbe, der Moon/Planet-Umschalter und alle Effekte
steuern. Alles liegt in **einem Block von 29 Kanälen**.

## Einrichten

Im Interface, oben (Parameter am Projekt-COMP `Frequenzfamilie1311`, Seite **DMX**):

| Parameter | Standard | Bedeutung |
|---|---|---|
| **Control Source** | Manual | `Manual`: die Regler im Interface gelten. `DMX (Art-Net)`: die Kanäle unten gelten. |
| **Net** | 0 | Art-Net Net (0-127) |
| **Subnet** | 0 | Art-Net Subnet (0-15) |
| **Universe** | 0 | Art-Net Universe (0-15) |
| **Start Channel** | 1 | Erster Kanal des 29er-Blocks (1-484) |
| **Network Adapter** | leer = alle | Auf welcher Netzwerkkarte (IP dieses Rechners) Art-Net gehört wird. Bei Problemen die Karte wählen, die im Netz des Pults liegt. |
| **Listening On** | (nur Anzeige) | Aktuelle Adresse, z.B. `Net 0 / Sub 0 / Uni 0 (Art-Net universe 0) channels 1-29` |
| **Channel Values** | (nur Anzeige) | Wie viele der 29 Kanäle gerade einen Wert über 0 haben. 0 = nichts (oder nur Nullen) angekommen. Zuletzt empfangene Werte bleiben stehen. |

Art-Net kommt per UDP auf Port 6454 an. Das Pult muss im selben Netz senden.

Ein Schalter für alles: bei `DMX (Art-Net)` ignorieren Farbwähler, Syphon-Output-Menü und alle Effekt-Regler
im Interface (sie ändern nichts, auch wenn man sie bewegt). Die Regler zeigen dann **nicht** die DMX-Werte an.

**Wichtig:** Kommt in DMX-Modus kein Signal an, stehen alle Kanäle auf 0 (Planet schwarz, Mond on air,
alle Effekte aus). Zum Zurückholen die Control Source wieder auf `Manual` stellen.

## Kanalbelegung

Kanal = Start Channel + Offset. In der Tabelle gilt Start Channel = 1.

Schalter (an/aus): 0-127 = aus, 128-255 = an.
Regler: der Wert 0-255 wird linear auf den Bereich gelegt.

| Kanal | Funktion | Werte |
|---|---|---|
| 1 | Planet Rot | 0-255 |
| 2 | Planet Grün | 0-255 |
| 3 | Planet Blau | 0-255 |
| 4 | **Output** (welches Element sendet Syphon) | 0-127 = Mond, 128-255 = Planet |
| 5 | Dither an/aus | Schalter |
| 6 | Dither Amount | 0 - 1 |
| 7 | Dither Colour Steps | 2 - 16 |
| 8 | Dither Dot Size | 3 - 64 px |
| 9 | Glitch an/aus | Schalter |
| 10 | Glitch Amount | 0 - 1 |
| 11 | Glitch Speed | 0.1 - 4 |
| 12 | Chromatische Aberration an/aus | Schalter |
| 13 | Chroma Amount | 0 - 1 |
| 14 | Bloom an/aus | Schalter |
| 15 | Bloom Amount | 0 - 3 |
| 16 | Bloom Threshold | 0 - 1 |
| 17 | Bloom Size | 4 - 128 px |
| 18 | ASCII an/aus | Schalter |
| 19 | ASCII Amount | 0 - 1 |
| 20 | ASCII Size | 6 - 48 px |
| 21 | Pulse (Zoom auf dem Beat) an/aus | Schalter |
| 22 | Pulse Amount | 0 - 0.3 |
| 23 | Flash auf dem Beat an/aus | Schalter |
| 24 | Flash Amount | 0 - 1 |
| 25 | Glitch nur auf dem Beat an/aus | Schalter |
| 26 | Swirl Kick (Planet) an/aus | Schalter |
| 27 | Swirl Kick Amount | 0 - 3 |
| 28 | Beat Decay (wie schnell der Impuls abklingt) | 1 - 12 |
| 29 | Beat Rate | 0-63 = halber Beat, 64-127 = jeder Beat, 128-191 = alle 2 Beats, 192-255 = jeder Takt |

Beispiel: Kanal 4 auf 0 schaltet auf den Mond um, Kanal 4 auf 255 zurück auf den Planeten. Der jeweils andere
pausiert (kein Rendering, Syphon-Server aus).

Bei anderem Start Channel verschiebt sich der ganze Block (Start Channel 10: Rot = 10, Output = 13, ASCII Size = 29, Beat Rate = 38).

## Beat (Ableton Link)

Der Beat kommt per **Ableton Link** (Seite **Beat** im Interface, rechts unten). `Ableton Link` ist standardmäßig
an: TouchDesigner tritt der Link-Session im Netz bei und folgt Tempo und Beat-Position. Läuft kein anderer
Link-Teilnehmer (Ableton Live, Resolume usw.), läuft die Uhr allein mit 120 BPM (Anzeige `running alone`).
Die Zeile **Link Status** zeigt, ob und mit wie vielen Teilnehmern verbunden wird und das Tempo.

Beat-Effekte (an/aus und Stärke auch über DMX, Kanäle 21-29): **Pulse** (Zoom), **Flash**, **Glitch nur auf dem Beat**,
**Swirl Kick** (die Wirbel des Planeten drehen auf dem Schlag stärker). **Beat Rate** legt fest, wie oft sie
feuern, **Beat Decay**, wie schnell der Impuls abklingt.

## Hinweise

- Die Planetenfarbe wirkt nur auf den Planeten. Der Mond bleibt grau.
- Die Effekte gelten für beide (Mond und Planet) und stehen vor dem Syphon-Ausgang.
- Alle Effekte sind auf den Kreis (Projektionsfläche) beschränkt.
- Schaltet das Pult den Output um, reagiert auch die Anzeige im Interface (`On Air (effective)`).

## Test ohne Pult

Ein Art-Net-Paket (Port 6454, Net 0 / Subnet 0 / Universe 0) mit Kanal 1-3 = 255 / 40 / 0 stellt den Planeten
rot. Die empfangenen Rohwerte (0-255) zeigt der CHOP `dmx/dmxin_all` (`c1` ... `c512`), die daraus berechneten
wirksamen Werte `dmx/null_control` (Namen: `r`, `g`, `b`, `output`, `glitch`, ...).

## Wo es technisch liegt

`/Frequenzfamilie1311/dmx`: `dmxin_all` (Empfang) -> `constant_dmx` (Kanäle -> Werte im jeweiligen Bereich)
und `constant_manual` (Werte aus den Interface-Parametern) -> `switch_source` (Control Source) ->
`null_control` (die wirksamen Werte). Planet (`planet/select_colour`), Effekte (`fx/glsl_*`) und
der Output-Schalter (`Onair` am Projekt-COMP) lesen nur noch `null_control`.
