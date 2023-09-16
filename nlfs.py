print("--- NLFS ---")
print("Natural Language FileSystem")
print("Version 1.0")
print("")
print("")

import openai, os, subprocess

try:
	openai.api_key = open("openaikey", "r").read()
except FileNotFoundError:
	openai.api_key = input("API Key: ")
	print("")
	print("")

msgs = [
		{"role": "system", "content": "You are a helpful assistant which can interact with the user's filesystem by getting information. All data inside the [PROMPT] tags is the user prompt and all data inside the [SYSTEM] tags is data given by the system for context."},
		{"role": "user", "content": """[PROMPT]Give me information about this folder[/PROMPT]
[DATA]
-- myprojects
   |-- jsoncats
   |-- aprogramminglang
   |-- minecraftrecreation
   |-- sideprojects
[DATA]"""},
		{"role": "assistant", "content": """- "jsoncats": This folder likely contains files related to a project or task involving JSON and cats. Without further details, it's unclear what specific content or purpose this folder serves.
- "aprogramminglang": Inside this folder, there may be files related to the development or exploration of a programming language. Again, the specifics of this project would require further investigation.
- "minecraftrecreation": This folder could contain materials related to recreating something within the popular video game Minecraft. It may include maps, textures, or other assets related to this recreation.
- "sideprojects": This folder could be a catch-all for various side projects that don't fit neatly into the other categories. The contents here could vary widely, and more information would be needed to understand the nature of these side projects."""},
		{"role": "user", "content": """[PROMPT]What static files are in this Git repo?/prompt]
[DATA]
-- pyratch
   |-- settings.json
   |-- LICENSE
   |-- interface.py
   |-- README.md
   |-- .gitignore
   |-- static
   |   |-- styles.css
   |-- CONTRIBUTING.md
   |-- templates
   |   |-- user_followers.html
   |   |-- root.html
   |   |-- user_projects.html
   |   |-- user_following.html
   |   |-- user.html
   |   |-- studio.html
   |   |-- project.html
   |   |-- settings.html
   |-- .git
   |   |-- ORIG_HEAD
   |   |-- config
   |   |-- objects
   |   |   |-- 58
   |   |   |   |-- a9ebb4311cd8484aa63ab096c56c4cbfdc94f2
   |   |   |-- 60
   |   |   |   |-- 0f74b20eba1aee274e3d4bea5b0da6f5230d91
   |   |   |-- a3
   |   |   |   |-- 25aa3d33f654f4aee927909f4b4b166019489b
   |   |   |-- a2
   |   |   |   |-- ba3c0c9b0dadaa5d3065a38e6faa8a2ad3f313
   |   |   |-- pack
   |   |   |   |-- pack-d92e899a06d0dd6074db3756b7fe6626a2418a2c.pack
   |   |   |   |-- pack-d92e899a06d0dd6074db3756b7fe6626a2418a2c.idx
   |   |   |-- 72
   |   |   |   |-- b0d46ccbd2651faf00a4477be2584b01594271
   |   |   |-- 00
   |   |   |   |-- 772ed36c8887a882f8f7c3dba9b1d9bfa37a8e
   |   |   |-- info
   |   |   |-- 54
   |   |   |   |-- 37843517e1c5fbe7ce057f5c4f3faa5f5e6807
   |   |   |-- 37
   |   |   |   |-- 5409dca838e5d0eb94bf77ef3b62e80b4d5eed
   |   |   |-- a7
   |   |   |   |-- 1df26632f46a6bf89ebc33330926bc355045c0
   |   |   |-- cc
   |   |   |   |-- faa0f2c27cca70209bde60f76186b2be1e7bd3
   |   |   |-- ff
   |   |   |   |-- 7792a8ebe76a5230f7fc4edf5eb19821c41d13
   |   |   |-- f8
   |   |   |   |-- be376d489d6a9b7fa4dccd7b0cddabfecec5e7
   |   |   |-- 8d
   |   |   |   |-- 61d9d89551ca7cf1d36e39ebc81ec5a221c6da
   |   |   |-- 2b
   |   |   |   |-- 25cdeba3778abb5caa189d7a8e62ad3cbd0b15
   |   |-- HEAD
   |   |-- info
   |   |   |-- exclude
   |   |-- logs
   |   |   |-- HEAD
   |   |   |-- refs
   |   |   |   |-- heads
   |   |   |   |   |-- dev
   |   |   |   |-- remotes
   |   |   |   |   |-- origin
   |   |   |   |   |   |-- zaid1442011mentioned-the-installer
   |   |   |   |   |   |-- HEAD
   |   |   |   |   |   |-- dev
   |   |-- description
   |   |-- hooks
   |   |   |-- commit-msg.sample
   |   |   |-- pre-rebase.sample
   |   |   |-- pre-commit.sample
   |   |   |-- applypatch-msg.sample
   |   |   |-- fsmonitor-watchman.sample
   |   |   |-- pre-receive.sample
   |   |   |-- prepare-commit-msg.sample
   |   |   |-- post-update.sample
   |   |   |-- pre-merge-commit.sample
   |   |   |-- pre-applypatch.sample
   |   |   |-- pre-push.sample
   |   |   |-- update.sample
   |   |-- refs
   |   |   |-- heads
   |   |   |   |-- dev
   |   |   |-- tags
   |   |   |-- remotes
   |   |   |   |-- origin
   |   |   |   |   |-- zaid1442011mentioned-the-installer
   |   |   |   |   |-- HEAD
   |   |   |   |   |-- dev
   |   |-- index
   |   |-- packed-refs
   |   |-- FETCH_HEAD
   |-- .pyratch-token
[/DATA]"""},
		{"role": "assistant", "content": """- "static": This folder contains a static CSS file for styling named `styles.css`.
		- "templates": This folder contains static HTML files for the Flask templates.
		In total there are 9 static files with 1 CSS file and 8 HTML files."""}
]

while True:
	inp = input("nlfs> ")
	if inp.startswith("/"):
		cmd = inp.split("/")[1].split(" ")[0]
		if cmd == "tree":
			arg1 = inp.split(" ")[1]
			arg2 = " ".join(inp.split(" ")[2:])
			tree_result = subprocess.check_output(f"tree {arg1}")
			msgs.append({"role": "user", "content": f"[PROMPT]{arg2}[PROMPT]\n[DATA]{tree_result}[DATA]"})
			resp = openai.ChatCompletion.create(
				model="gpt-3.5-turbo",
				messages=msgs
			)
			msgs.append(resp["choices"]["message"])
			print("AI: " + msgs[-1]["content"])
		elif cmd == "list":
			arg1 = inp.split(" ")[1]
			arg2 = " ".join(inp.split(" ")[2:])
			list_result = subprocess.check_output(f"ls {arg1}")
			msgs.append({"role": "user", "content": f"[PROMPT]{arg2}[PROMPT]\n[DATA]{list_result}[DATA]"})
			resp = openai.ChatCompletion.create(
				model="gpt-3.5-turbo",
				messages=msgs
			)
			msgs.append(resp["choices"]["message"])
			print("AI: " + msgs[-1]["content"])
		else:
			print("NLFS: There is no command named that")
	else:
		continue
