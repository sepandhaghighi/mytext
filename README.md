<div align="center">
<img src="https://github.com/sepandhaghighi/mytext/raw/main/otherfiles/logo.png" width="350">
<h1>MyText: A Minimal AI-Powered Text Rewriting Tool</h1>
<br/>
<a href="https://codecov.io/gh/sepandhaghighi/mytext"><img src="https://codecov.io/gh/sepandhaghighi/mytext/graph/badge.svg?token=qNCcVof7QW"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/built%20with-Python3-green.svg" alt="built with Python3"></a>
<a href="https://github.com/sepandhaghighi/mytext"><img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/sepandhaghighi/mytext"></a>
<a href="https://badge.fury.io/py/mytext"><img src="https://badge.fury.io/py/mytext.svg" alt="PyPI version"></a>
</div>			
				
## Overview	

<p align="justify">		
<b>MyText</b> is a lightweight AI-powered text enhancement tool that rewrites, paraphrases, and adjusts tone using modern LLM providers. It offers a clean command-line interface and a minimal Python API, supports multiple providers (Google AI Studio & Cloudflare Workers AI), and automatically selects the first available provider based on your environment variables.
</p>

<table>
	<tr>
		<td align="center">PyPI Counter</td>
		<td align="center"><a href="http://pepy.tech/project/mytext"><img src="http://pepy.tech/badge/mytext"></a></td>
	</tr>
	<tr>
		<td align="center">Github Stars</td>
		<td align="center"><a href="https://github.com/sepandhaghighi/mytext"><img src="https://img.shields.io/github/stars/sepandhaghighi/mytext.svg?style=social&label=Stars"></a></td>
	</tr>
</table>



<table>
	<tr> 
		<td align="center">Branch</td>
		<td align="center">main</td>	
		<td align="center">dev</td>	
	</tr>
	<tr>
		<td align="center">CI</td>
		<td align="center"><img src="https://github.com/sepandhaghighi/mytext/actions/workflows/test.yml/badge.svg?branch=main"></td>
		<td align="center"><img src="https://github.com/sepandhaghighi/mytext/actions/workflows/test.yml/badge.svg?branch=dev"></td>
	</tr>
</table>
<table>
    <tr> 
        <td align="center">Code Quality</td>
        <td align="center"><a href="https://www.codefactor.io/repository/github/sepandhaghighi/mytext"><img src="https://www.codefactor.io/repository/github/sepandhaghighi/mytext/badge" alt="CodeFactor"></a></td>
        <td align="center"><a href="https://app.codacy.com/gh/sepandhaghighi/mytext/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade"><img src="https://app.codacy.com/project/badge/Grade/239efecb91c0428693c3ec744853aff5"></a></td>
    </tr>
</table>

## Installation		

### Source Code
- Download [Version 0.4](https://github.com/sepandhaghighi/mytext/archive/v0.4.zip) or [Latest Source](https://github.com/sepandhaghighi/mytext/archive/dev.zip)
- `pip install .`				

### PyPI

- Check [Python Packaging User Guide](https://packaging.python.org/installing/)     
- `pip install mytext==0.4`						


## Usage

### CLI

#### Single Run

Executes a one-time text transformation using the provided options and exits immediately after producing the result.

```bash
mytext \
  --mode="paraphrase" \
  --tone="formal" \
  --text="Can you update me on the project timeline by the end of the day?"
```

#### Loop

Starts an interactive session that repeatedly accepts new text inputs from the user while keeping the same configuration until the process is terminated.

```bash
mytext \
  --mode="paraphrase" \
  --tone="formal" \
  --loop
```


ℹ️ Supported modes: `paraphrase`, `grammar`, `summarize`, `simplify`, `bulletize`, `shorten`

ℹ️ Supported tones: `neutral`, `formal`, `casual`, `friendly`, `professional`, `academic`, `creative`

### Library

You can also use MyText directly inside Python.

```python
from mytext import run_mytext
from mytext import Mode, Tone, Provider

auth = {"api_key": "YOUR_KEY"}
result = run_mytext(
    text="Let me know if you have any questions after reviewing the attached document.",
    auth=auth,
    mode=Mode.PARAPHRASE,
    tone=Tone.NEUTRAL,
    provider=Provider.AI_STUDIO
)

print(result["status"], result["message"])
```

## Supported Providers

MyText automatically detects which providers are available based on environment variables:

| Provider | Required Environment Variables | Main Model | Fallback Model |
|---------|--------------------------------|------------|----------------|
| [**AI Studio**](https://ai.google.dev/) | `AI_STUDIO_API_KEY` | `gemini-2.5-flash` | `gemma-3-1b-it` |
| [**Cloudflare**](https://developers.cloudflare.com/workers-ai/) | `CLOUDFLARE_API_KEY`, `CLOUDFLARE_ACCOUNT_ID` | `meta/llama-3-8b-instruct` | `meta/llama-3.1-8b-instruct-fast` |
| [**OpenRouter**](https://openrouter.ai/docs) | `OPENROUTER_API_KEY` | `mistralai/mistral-small-3.1-24b-instruct:free` | `google/gemma-3-27b-it:free` |
| [**Cerebras**](https://docs.cerebras.ai/) | `CEREBRAS_API_KEY` | `gpt-oss-120b` | `llama-3.3-70b` |
| [**Groq**](https://console.groq.com/docs) | `GROQ_API_KEY` | `openai/gpt-oss-20b` | `llama-3.1-8b-instant` |
| [**NVIDIA**](https://docs.nvidia.com/nim/) | `NVIDIA_API_KEY` | `meta/llama-3.1-8b-instruct` | `meta/llama3-8b-instruct` |

Set them before using:

```bash
export AI_STUDIO_API_KEY="your-key"
export CLOUDFLARE_API_KEY="your-key"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
export OPENROUTER_API_KEY="your-key"
export CEREBRAS_API_KEY="your-key"
export GROQ_API_KEY="your-key"
export NVIDIA_API_KEY="your-key"
```

## Issues & Bug Reports			

Just fill an issue and describe it. We'll check it ASAP!

- Please complete the issue template

## Show Your Support
								
<h3>Star This Repo</h3>					

Give a ⭐️ if this project helped you!

<h3>Donate to Our Project</h3>	

<h4>Bitcoin</h4>
1KtNLEEeUbTEK9PdN6Ya3ZAKXaqoKUuxCy
<h4>Ethereum</h4>
0xcD4Db18B6664A9662123D4307B074aE968535388
<h4>Litecoin</h4>
Ldnz5gMcEeV8BAdsyf8FstWDC6uyYR6pgZ
<h4>Doge</h4>
DDUnKpFQbBqLpFVZ9DfuVysBdr249HxVDh
<h4>Tron</h4>
TCZxzPZLcJHr2qR3uPUB1tXB6L3FDSSAx7
<h4>Ripple</h4>
rN7ZuRG7HDGHR5nof8nu5LrsbmSB61V1qq
<h4>Binance Coin</h4>
bnb1zglwcf0ac3d0s2f6ck5kgwvcru4tlctt4p5qef
<h4>Tether</h4>
0xcD4Db18B6664A9662123D4307B074aE968535388
<h4>Dash</h4>
Xd3Yn2qZJ7VE8nbKw2fS98aLxR5M6WUU3s
<h4>Stellar</h4>		
GALPOLPISRHIYHLQER2TLJRGUSZH52RYDK6C3HIU4PSMNAV65Q36EGNL
<h4>Zilliqa</h4>
zil1knmz8zj88cf0exr2ry7nav9elehxfcgqu3c5e5
<h4>Coffeete</h4>
<a href="http://www.coffeete.ir/opensource">
<img src="http://www.coffeete.ir/images/buttons/lemonchiffon.png" style="width:260px;" />
</a>

