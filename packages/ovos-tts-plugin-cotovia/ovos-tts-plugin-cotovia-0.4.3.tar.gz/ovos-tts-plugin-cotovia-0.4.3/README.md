## Description

OVOS TTS plugin for [Cotovia TTS](http://gtm.uvigo.es/cotovia)

### About Cotovia

Cotovia is a unit-selection text-to-speech system, i.e., generates the synthetic speech signal as a
concatenation of prerecorded segments. Cotovia determines the sequence of sounds, its intonation and 
duration from the input text. Actually several intonation contours are considered in parallel and for
each one a sequence of speech units is selected. The final intonation contours is selected according to 
the suitability of the sequence of speech units found.
 
### Voices

At this time two Galician voices are available at sourceforge. These two voices are also suitable for Spanish,
 with little distortion, since the phonemes of Spanish may be considered a subset of Galician phonemes. The
 nicknames of the two speakers are Iago and Sabela. Nevertheless you will find three voices available for
 Cotovia:

* iago : Galician male speaker, duration of the recording: 80 minutes. It was Cotovia's first voice and the
 quality is limited by the reduced recording time.

* sabela-large : Galician female speaker, duration of the recording: 14.5 hours. Use this voice if you want to
 obtain maximum quality speech and you are not too worried about execution time.

* sabela: default speaker. A subset of Sabela's recordings (about 4 hours). A good compromise between quality
 and execution time.
 

## Install

Install the plugin

`pip install ovos-tts-plugin-cotovia`

Download and install [Cotovia](https://sourceforge.net/projects/cotovia/files/Debian%20packages/)

#### Debian

In order to run Cotovia, you will need to install the following packages:

    cotovia_0.5_amd64.deb   ---  Cotovia executable
    cotovia-lang-gl_0.5_all.deb --- Galician linguistic data
    cotovia-lang-es_0.5_all.deb --- Spanish linguistic data

Additionally you need to install at least one voice

    cotovia-voice-iago_0.5_all.deb
    cotovia-voice-sabela-large_0.5_all.deb
    cotovia-voice-sabela_0.5_all.deb

#### Arch

arch linux users can find packages converted with 'debtap' in the [releases page](https://github.com/OpenVoiceOS/ovos-tts-plugin-cotovia/releases/tag/0.4.1)

```bash
sudo pacman -U /home/miro/Transferências/cotovia-0.5-1-x86_64.pkg.tar.zst
sudo pacman -U /home/miro/Transferências/cotovia-lang-es-0.5-1-any.pkg.tar.zst 
sudo pacman -U /home/miro/Transferências/cotovia-lang-gl-0.5-1-any.pkg.tar.zst 
sudo pacman -U /home/miro/Transferências/cotovia-voice-iago-0.5-1-any.pkg.tar.zst 
sudo pacman -U /home/miro/Transferências/cotovia-voice-sabela-0.5-1-any.pkg.tar.zst 
sudo pacman -U /home/miro/Transferências/cotovia-voice-sabela-large-0.5-1-any.pkg.tar.zst 
```

otherwise here is a guide [how to install a .deb package in arch linux](https://www.baeldung.com/linux/arch-install-deb-package)

## Configuration

```json
  "tts": {
    "module": "ovos-tts-plugin-cotovia",
    "ovos-tts-plugin-cotovia": {
      "voice": "iago"
    }
  }
 
```

### Advanced config

Additional configuration params are available

- `lang` can be `gl` for galician or `es` 
- `voice` cab be `iago` or `sabela`
- `pitch_scale_factor` can be used to change pitch (default `100`)
- `time_scale_factor` can be used to change speed (default `100`)
- `bin` can be used to set a path to the executable (default `/usr/bin/cotovia`)

```json
  "tts": {
    "module": "ovos-tts-plugin-cotovia",
    "ovos-tts-plugin-cotovia": {
      "voice": "sabela",
      "lang": "es",
      "pitch_scale_factor": 80,
      "time_scale_factor": 80,
      "bin": "/usr/bin/cotovia"
    }
   }
 
```


