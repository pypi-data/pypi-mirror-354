
# Changelog



## [0.0.5](https://github.com/x55xaa/arduck/compare/v0.0.3...v0.0.5) - 2025-05-27

### Added

- Add some useful `jinja2` filters ([7ca9cf3](https://github.com/x55xaa/arduck/commit/7ca9cf3a1dce9b41a0f711394425a6238d7b1684)) - (Stefano Cuizza)
- Add Windows ALT codes template ([6161a45](https://github.com/x55xaa/arduck/commit/6161a452fb6f58fd70318583581599e46d623020)) - (Stefano Cuizza)
- Add Windows run dialog template ([e26927d](https://github.com/x55xaa/arduck/commit/e26927d89244138ab146274f5e0518eb2fb1da52)) - (Stefano Cuizza)
- Add Windows x-menu admin terminal template ([3f0968b](https://github.com/x55xaa/arduck/commit/3f0968bdcb8649a573c1bd13d954c9931f2bdf07)) - (Stefano Cuizza)

### Changed

- Include keyboard layout specific special keys when selecting a non-standard layout ([51d51ca](https://github.com/x55xaa/arduck/commit/51d51ca852925b17fd1626b6426b76d60ee72dd6)) - (Stefano Cuizza)

### Fixed

- Remove `CAPS_LOCK` optimization from parser ([716f671](https://github.com/x55xaa/arduck/commit/716f671a8802a7b21fd89d228acd738c559e06bf)) - (Stefano Cuizza)
- Better template type check ([4d6690f](https://github.com/x55xaa/arduck/commit/4d6690fed53a1aa6f1db696ad9a929b71ee2f70f)) - (Stefano Cuizza)
- Add ability to select `init` templates ([b882147](https://github.com/x55xaa/arduck/commit/b882147eeff57732d506f1a8b5ad0379991e494b)) - (Stefano Cuizza)
- Add break in switch case to avoid accumulating delays ([d06f0d4](https://github.com/x55xaa/arduck/commit/d06f0d4805ce06af2b8c1fbc0513dca5f90d208e)) - (Stefano Cuizza)


## [0.0.3](https://github.com/x55xaa/arduck/compare/v0.0.1...v0.0.3) - 2025-05-20

### Fixed

- Recognize special keys containing numbers ([0771b54](https://github.com/x55xaa/arduck/commit/0771b54b6d9f633960a56b42fe57529970d3cc3f)) - (Stefano Cuizza)
- Recognize combos comprised of more than two keys ([efceed2](https://github.com/x55xaa/arduck/commit/efceed2f4e3c1292c8c0960229e03244c9ecaa4d)) - (Stefano Cuizza)
- Better shift correction for combos ([3f39a45](https://github.com/x55xaa/arduck/commit/3f39a45623315c88affc3fb3c525a1f0fc267734)) - (Stefano Cuizza)


## [0.0.1](https://github.com/x55xaa/arduck/releases/tag/v0.0.1) - 2025-05-20

_🌱 Initial release._

### Added

- Add supported keyboard layouts and special keys ([d268d72](https://github.com/x55xaa/arduck/commit/d268d722fdea1ce42b5739f5a62c00ef2d90b9a7)) - (Stefano Cuizza)
- Add a CLI ([5c6af0c](https://github.com/x55xaa/arduck/commit/5c6af0c540929977aa695e4ab646415cb1a0843e)) - (Stefano Cuizza)
- Add templates ([9c3aabf](https://github.com/x55xaa/arduck/commit/9c3aabf5d8f5670315d617321245feab78b67364)) - (Stefano Cuizza)
- Add default template ([1211b14](https://github.com/x55xaa/arduck/commit/1211b149f1ddf6157936b0b004c74ddee959279c)) - (Stefano Cuizza)
- Add ability to specify template through the CLI ([d8f8fa4](https://github.com/x55xaa/arduck/commit/d8f8fa42e5a12adddbf42e8047cf92b78d7b959b)) - (Stefano Cuizza)
- Add ability to repeat injection in a loop ([7e2cf36](https://github.com/x55xaa/arduck/commit/7e2cf3615eaaccc197428efcb7bf0a2a7ad37dda)) - (Stefano Cuizza)

### Changed

- Flatten one character combos ([b94e5db](https://github.com/x55xaa/arduck/commit/b94e5db63c23496bfc182819d494c3bc0b4bec57)) - (Stefano Cuizza)
- Merge consecutive delays ([fa1c365](https://github.com/x55xaa/arduck/commit/fa1c3658e01f07018efaf4e6dcb397ce0ecdec8f)) - (Stefano Cuizza)

### Fixed

- Tokenizer now translates special keys correctly ([f1c92e0](https://github.com/x55xaa/arduck/commit/f1c92e0f8839cedce491a92bb3dde299466d7c83)) - (Stefano Cuizza)
- Add shift correction to counter index mismatch ([f768fb4](https://github.com/x55xaa/arduck/commit/f768fb4f49cf8085ea5b6bad49084e7125356778)) - (Stefano Cuizza)
- Change default outfile to `sketch.ino` ([7089673](https://github.com/x55xaa/arduck/commit/708967396441d495e30dc1d280230a855db7c473)) - (Stefano Cuizza)
- The `any.default` template can now handle delays that appear right before the end of the injection ([674144e](https://github.com/x55xaa/arduck/commit/674144e32b2f3386ac57fd2d0471368dc23362e1)) - (Stefano Cuizza)

