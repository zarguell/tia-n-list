The MALFEX campaign continues to evolve through malicious npm packages. The package imgdecode, uploaded by publisher malfexteste8 on September 30, 2026, contains a compiled Node.js addon that acts as a loader. Nine lines of JavaScript load a Windows DLL, hiding the malicious payload inside a native binary. SafeDep and additional reports have tracked this supply-chain activity.

Why it matters: Native-addon loaders bypass many static-analysis and dependency-scanning tools because the malicious code lives in a compiled binary rather than JavaScript. Organizations relying on npm packages for build pipelines should audit compiled dependencies and monitor for unexpected native modules.

What to watch: whether the campaign expands to additional publishers, whether npm registry maintainers remove the package and related accounts, and whether similar native-addon patterns appear in other ecosystem registries like PyPI or RubyGems.
