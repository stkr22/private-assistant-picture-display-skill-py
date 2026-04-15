# Changelog

## [0.14.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.13.1...v0.14.0) (2026-04-15)


### Features

* :recycle: delegate device and image management to display API ([e0eb234](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/e0eb234eceba8e5e4b07013bec9f71434f25a09f))
* :recycle: delegate device and image management to display API ([5dd016f](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/5dd016fe03b5898431f354339606b6fac2063034))


### Bug Fixes

* :wrench: restore single-package CI workflows from monorepo matrix ([891fbb5](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/891fbb594c9326daa57b5cd40eced03e36e7d59d))

## [0.13.1](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.13.0...v0.13.1) (2026-04-11)


### Bug Fixes

* :bug: use weighted formula for vibrancy score instead of max ([04bdfc3](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/04bdfc33c9ef0de6749051e6b5c9ac8d2661c72f))
* :bug: use weighted formula for vibrancy score instead of max ([e259717](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/e25971723596e6e20e045244415161c500dd151b))

## [0.13.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.12.1...v0.13.0) (2026-04-11)


### Features

* :sparkles: add vibrancy filter to reject dull/dark images for e-ink ([daab419](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/daab419f73a9a9c94257bf942a19805c6849cc34))
* :sparkles: add vibrancy filter to reject dull/dark images for e-ink ([c7169ce](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/c7169ce4ab9506597b9a7b66f66e507d3f053ece))

## [0.12.1](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.12.0...v0.12.1) (2026-04-11)


### Bug Fixes

* :bug: use top-level asset dimensions for orientation filtering ([075fc0a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/075fc0a0c0ba01ef911156055fea76dbf780cbcb))
* :bug: use top-level asset dimensions for orientation filtering ([55ae469](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/55ae4693e52e26d12b2da7f37c16a8dd67fb7bf5))

## [0.12.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.11.1...v0.12.0) (2026-04-11)


### Features

* :arrow_up: update to latest copier template and migrate help text ([149e78b](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/149e78b604c620a5ffc67b8fc38dfe24f916f326))
* :arrow_up: update to latest copier template and migrate help text ([ab9ade2](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ab9ade24146e6231c6b6070816aa1d03a7959df2))
* :card_file_box: add database models and skill configuration ([f1883f1](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/f1883f1e15512bdb2f732ce4250c81bc90c9d29e))
* :lock: require explicit config values, remove unsafe defaults ([e621ac0](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/e621ac02323a4168ceb1b759703da8117415f563))
* :recycle: add expires_at-based image retention to immich sync ([8681b6a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8681b6a46787b2ae8869f240ee9067fd64dd0c4f))
* :recycle: modernize infrastructure with create_skill_engine and MqttConfig [AI] ([c14d008](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/c14d0080642c21872c94ebf480ddc1d84f6b122e)), closes [#31](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/31)
* :recycle: update devcontainer configuration and improve .gitignore ([50d24db](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/50d24db43b16c4af8246e33f2a889009d9de0bec))
* :sparkles: add configurable S3 region and rename Minio* to S3* ([8e0f492](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8e0f492a7081465f213f7c1382643f6805a227ba))
* :sparkles: add configurable total image limit for Immich sync [AI] ([325cb67](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/325cb6764bb3ce975531a298827d0a8d2260321b))
* :sparkles: add immich sync integration for image sourcing [AI] ([378d0b3](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/378d0b30326cbb281c29d43fb086d9b1e5c3db3f))
* :sparkles: add tags, created_at, updated_at to Image model [AI] ([0998c34](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/0998c34fb28fec267c81e79e0eec964371d3d39b)), closes [#32](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/32)
* :sparkles: implement PictureSkill with voice commands and rotation ([9a1b020](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/9a1b0201b17f9aedcd49ada09de0b15397626d27)), closes [#4](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/4)
* :sparkles: refresh all devices in a room on next picture command ([fdbe141](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/fdbe141b232c1517d47267a29963a78334a317f7))
* :sparkles: rename minio_* fields to s3_* in RegistrationResponse ([8d8e22c](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8d8e22c5efcf55b364762d3d90aabe354f231968))
* :sparkles: rename minio_* fields to s3_* in RegistrationResponse ([36d650d](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/36d650dea9c419f7db6cd006fe72ca58e8049176))
* :wrench: add pydantic mypy plugin for settings validation [AI] ([79aeef6](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/79aeef690be8baf022ac3c44f290d6f7de342332))
* :zap: add device MQTT client and image manager services ([3636ea4](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/3636ea480dc8635669912252bbe8e1f1f496a83d)), closes [#4](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/4)
* add tags, created_at, updated_at fields to Image model ([4a0b47b](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/4a0b47b8df897095a53cca073bba2681cc0b9bda))
* implement picture display skill with integration tests ([e6e8e7a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/e6e8e7a1928cc52bdd896baf9249d88b87a5f860))
* modernize infrastructure with create_skill_engine and MqttConfig ([9a9ec91](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/9a9ec9133406b5cf80c9ea2e858ac967a5f9d62b))


### Bug Fixes

* :bug: store processed dimensions and require exact match for image selection [AI] ([5890339](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/589033972b4e33977fdda3e544170d69d6236bf1))
* :bug: store processed dimensions and require exact match for image selection [AI] ([a13d877](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/a13d87730c3b23d992b3fdff90d9b8aeb57a5696))
* :bug: swap dimensions for portrait devices in image selection and sync ([9ebbb80](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/9ebbb8004ea42dfbfa82dfddbda2b36e3d2c961e))
* :bug: swap dimensions for portrait devices in image selection and sync ([4737bf4](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/4737bf4281158068f12b829fc104c00cc9379f9d))
* :bug: update default display duration to 10 minutes ([b85aacf](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/b85aacfcb06509d5a96904c8ecede19980cf5b70))
* :sparkles: add workspaceFolder configuration to development container ([b365054](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/b36505416945f147fc8cb948982cb1d6683e5db3))
* :wrench: correct devcontainer volume mount and workspaceFolder ([ac08778](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ac08778108895ad86ee2b24111a37bb957adcdba))
* **deps:** update dependency typer to ~=0.21.0 ([cdcea8a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/cdcea8a6e8034a0f86983d7f31fdd1885cc5e4a5))
* **deps:** update dependency typer to ~=0.21.0 ([ceab4bb](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ceab4bb9187a4fee1a248d08f81cd1b542111419))
* **deps:** update minor updates ([dfcd627](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/dfcd627da7924e32541e9cca573ff60d0d53cf12))
* **deps:** update minor updates ([dbc20b7](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/dbc20b771bed472c562f7d390b04ce560107dd5e))
* raw text select issue ([bf71862](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/bf7186286f3f51c0d2b55b647a808cef51cb429d))
* update default priority for image selection ([85dabbf](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/85dabbfc0ebfc959ee54c2a26e580b9e018fa93c))


### Documentation

* :memo: add configuration and deployment documentation ([eb6c275](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/eb6c2756cf89c717c662fd7ef6905af1a8a9b8c0)), closes [#5](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/5)
* :memo: update container and docs for immich-sync command [AI] ([0063ebb](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/0063ebb41643fc7833269c553ac10c15ac1f904a))

## [0.11.1](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.11.0...v0.11.1) (2026-04-11)


### Bug Fixes

* :bug: swap dimensions for portrait devices in image selection and sync ([9ebbb80](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/9ebbb8004ea42dfbfa82dfddbda2b36e3d2c961e))
* :bug: swap dimensions for portrait devices in image selection and sync ([4737bf4](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/4737bf4281158068f12b829fc104c00cc9379f9d))

## [0.11.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.10.0...v0.11.0) (2026-04-11)


### Features

* :arrow_up: update to latest copier template and migrate help text ([149e78b](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/149e78b604c620a5ffc67b8fc38dfe24f916f326))
* :arrow_up: update to latest copier template and migrate help text ([ab9ade2](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ab9ade24146e6231c6b6070816aa1d03a7959df2))
* :card_file_box: add database models and skill configuration ([f1883f1](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/f1883f1e15512bdb2f732ce4250c81bc90c9d29e))
* :lock: require explicit config values, remove unsafe defaults ([e621ac0](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/e621ac02323a4168ceb1b759703da8117415f563))
* :recycle: add expires_at-based image retention to immich sync ([8681b6a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8681b6a46787b2ae8869f240ee9067fd64dd0c4f))
* :recycle: modernize infrastructure with create_skill_engine and MqttConfig [AI] ([c14d008](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/c14d0080642c21872c94ebf480ddc1d84f6b122e)), closes [#31](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/31)
* :recycle: update devcontainer configuration and improve .gitignore ([50d24db](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/50d24db43b16c4af8246e33f2a889009d9de0bec))
* :sparkles: add configurable S3 region and rename Minio* to S3* ([8e0f492](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8e0f492a7081465f213f7c1382643f6805a227ba))
* :sparkles: add configurable total image limit for Immich sync [AI] ([325cb67](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/325cb6764bb3ce975531a298827d0a8d2260321b))
* :sparkles: add immich sync integration for image sourcing [AI] ([378d0b3](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/378d0b30326cbb281c29d43fb086d9b1e5c3db3f))
* :sparkles: add tags, created_at, updated_at to Image model [AI] ([0998c34](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/0998c34fb28fec267c81e79e0eec964371d3d39b)), closes [#32](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/32)
* :sparkles: implement PictureSkill with voice commands and rotation ([9a1b020](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/9a1b0201b17f9aedcd49ada09de0b15397626d27)), closes [#4](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/4)
* :sparkles: refresh all devices in a room on next picture command ([fdbe141](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/fdbe141b232c1517d47267a29963a78334a317f7))
* :sparkles: rename minio_* fields to s3_* in RegistrationResponse ([8d8e22c](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8d8e22c5efcf55b364762d3d90aabe354f231968))
* :sparkles: rename minio_* fields to s3_* in RegistrationResponse ([36d650d](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/36d650dea9c419f7db6cd006fe72ca58e8049176))
* :wrench: add pydantic mypy plugin for settings validation [AI] ([79aeef6](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/79aeef690be8baf022ac3c44f290d6f7de342332))
* :zap: add device MQTT client and image manager services ([3636ea4](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/3636ea480dc8635669912252bbe8e1f1f496a83d)), closes [#4](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/4)
* add tags, created_at, updated_at fields to Image model ([4a0b47b](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/4a0b47b8df897095a53cca073bba2681cc0b9bda))
* implement picture display skill with integration tests ([e6e8e7a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/e6e8e7a1928cc52bdd896baf9249d88b87a5f860))
* modernize infrastructure with create_skill_engine and MqttConfig ([9a9ec91](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/9a9ec9133406b5cf80c9ea2e858ac967a5f9d62b))


### Bug Fixes

* :bug: store processed dimensions and require exact match for image selection [AI] ([5890339](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/589033972b4e33977fdda3e544170d69d6236bf1))
* :bug: store processed dimensions and require exact match for image selection [AI] ([a13d877](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/a13d87730c3b23d992b3fdff90d9b8aeb57a5696))
* :bug: update default display duration to 10 minutes ([b85aacf](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/b85aacfcb06509d5a96904c8ecede19980cf5b70))
* :sparkles: add workspaceFolder configuration to development container ([b365054](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/b36505416945f147fc8cb948982cb1d6683e5db3))
* :wrench: correct devcontainer volume mount and workspaceFolder ([ac08778](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ac08778108895ad86ee2b24111a37bb957adcdba))
* **deps:** update dependency typer to ~=0.21.0 ([cdcea8a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/cdcea8a6e8034a0f86983d7f31fdd1885cc5e4a5))
* **deps:** update dependency typer to ~=0.21.0 ([ceab4bb](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ceab4bb9187a4fee1a248d08f81cd1b542111419))
* **deps:** update minor updates ([dfcd627](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/dfcd627da7924e32541e9cca573ff60d0d53cf12))
* **deps:** update minor updates ([dbc20b7](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/dbc20b771bed472c562f7d390b04ce560107dd5e))
* raw text select issue ([bf71862](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/bf7186286f3f51c0d2b55b647a808cef51cb429d))
* update default priority for image selection ([85dabbf](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/85dabbfc0ebfc959ee54c2a26e580b9e018fa93c))


### Documentation

* :memo: add configuration and deployment documentation ([eb6c275](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/eb6c2756cf89c717c662fd7ef6905af1a8a9b8c0)), closes [#5](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/5)
* :memo: update container and docs for immich-sync command [AI] ([0063ebb](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/0063ebb41643fc7833269c553ac10c15ac1f904a))

## [0.10.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.9.0...v0.10.0) (2026-04-11)


### Features

* :sparkles: refresh all devices in a room on next picture command ([fdbe141](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/fdbe141b232c1517d47267a29963a78334a317f7))


### Bug Fixes

* :sparkles: add workspaceFolder configuration to development container ([b365054](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/b36505416945f147fc8cb948982cb1d6683e5db3))
* :wrench: correct devcontainer volume mount and workspaceFolder ([ac08778](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ac08778108895ad86ee2b24111a37bb957adcdba))

## [0.9.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.8.0...v0.9.0) (2026-04-02)


### Features

* :sparkles: rename minio_* fields to s3_* in RegistrationResponse ([8d8e22c](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8d8e22c5efcf55b364762d3d90aabe354f231968))
* :sparkles: rename minio_* fields to s3_* in RegistrationResponse ([36d650d](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/36d650dea9c419f7db6cd006fe72ca58e8049176))

## [0.8.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.7.0...v0.8.0) (2026-04-02)


### Features

* :sparkles: add configurable S3 region and rename Minio* to S3* ([8e0f492](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8e0f492a7081465f213f7c1382643f6805a227ba))

## [0.7.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.6.0...v0.7.0) (2026-02-23)


### Features

* :recycle: add expires_at-based image retention to immich sync ([8681b6a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/8681b6a46787b2ae8869f240ee9067fd64dd0c4f))

## [0.6.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.5.0...v0.6.0) (2026-01-31)


### Features

* :arrow_up: update to latest copier template and migrate help text ([149e78b](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/149e78b604c620a5ffc67b8fc38dfe24f916f326))
* :arrow_up: update to latest copier template and migrate help text ([ab9ade2](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ab9ade24146e6231c6b6070816aa1d03a7959df2))

## [0.5.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.4.4...v0.5.0) (2026-01-19)


### Features

* :sparkles: add configurable total image limit for Immich sync [AI] ([325cb67](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/325cb6764bb3ce975531a298827d0a8d2260321b))

## [0.4.4](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.4.3...v0.4.4) (2026-01-13)


### Bug Fixes

* :bug: store processed dimensions and require exact match for image selection [AI] ([5890339](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/589033972b4e33977fdda3e544170d69d6236bf1))
* :bug: store processed dimensions and require exact match for image selection [AI] ([a13d877](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/a13d87730c3b23d992b3fdff90d9b8aeb57a5696))

## [0.4.3](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.4.2...v0.4.3) (2026-01-12)


### Bug Fixes

* update default priority for image selection ([85dabbf](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/85dabbfc0ebfc959ee54c2a26e580b9e018fa93c))

## [0.4.2](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.4.1...v0.4.2) (2026-01-12)


### Bug Fixes

* raw text select issue ([bf71862](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/bf7186286f3f51c0d2b55b647a808cef51cb429d))

## [0.4.1](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.4.0...v0.4.1) (2026-01-12)


### Bug Fixes

* :bug: update default display duration to 10 minutes ([b85aacf](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/b85aacfcb06509d5a96904c8ecede19980cf5b70))

## [0.4.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.3.0...v0.4.0) (2026-01-11)


### Features

* :sparkles: add immich sync integration for image sourcing [AI] ([378d0b3](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/378d0b30326cbb281c29d43fb086d9b1e5c3db3f))


### Documentation

* :memo: update container and docs for immich-sync command [AI] ([0063ebb](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/0063ebb41643fc7833269c553ac10c15ac1f904a))

## [0.3.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.2.0...v0.3.0) (2026-01-02)


### Features

* :recycle: modernize infrastructure with create_skill_engine and MqttConfig [AI] ([c14d008](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/c14d0080642c21872c94ebf480ddc1d84f6b122e)), closes [#31](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/31)
* :recycle: update devcontainer configuration and improve .gitignore ([50d24db](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/50d24db43b16c4af8246e33f2a889009d9de0bec))
* modernize infrastructure with create_skill_engine and MqttConfig ([9a9ec91](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/9a9ec9133406b5cf80c9ea2e858ac967a5f9d62b))

## [0.2.0](https://github.com/stkr22/private-assistant-picture-display-skill-py/compare/v0.1.0...v0.2.0) (2026-01-01)


### Features

* :lock: require explicit config values, remove unsafe defaults ([e621ac0](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/e621ac02323a4168ceb1b759703da8117415f563))
* :sparkles: add tags, created_at, updated_at to Image model [AI] ([0998c34](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/0998c34fb28fec267c81e79e0eec964371d3d39b)), closes [#32](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/32)
* :wrench: add pydantic mypy plugin for settings validation [AI] ([79aeef6](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/79aeef690be8baf022ac3c44f290d6f7de342332))
* add tags, created_at, updated_at fields to Image model ([4a0b47b](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/4a0b47b8df897095a53cca073bba2681cc0b9bda))


### Bug Fixes

* **deps:** update dependency typer to ~=0.21.0 ([cdcea8a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/cdcea8a6e8034a0f86983d7f31fdd1885cc5e4a5))
* **deps:** update dependency typer to ~=0.21.0 ([ceab4bb](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/ceab4bb9187a4fee1a248d08f81cd1b542111419))
* **deps:** update minor updates ([dfcd627](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/dfcd627da7924e32541e9cca573ff60d0d53cf12))
* **deps:** update minor updates ([dbc20b7](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/dbc20b771bed472c562f7d390b04ce560107dd5e))

## 0.1.0 (2025-12-13)


### Features

* :card_file_box: add database models and skill configuration ([f1883f1](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/f1883f1e15512bdb2f732ce4250c81bc90c9d29e))
* :sparkles: implement PictureSkill with voice commands and rotation ([9a1b020](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/9a1b0201b17f9aedcd49ada09de0b15397626d27)), closes [#4](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/4)
* :zap: add device MQTT client and image manager services ([3636ea4](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/3636ea480dc8635669912252bbe8e1f1f496a83d)), closes [#4](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/4)
* implement picture display skill with integration tests ([e6e8e7a](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/e6e8e7a1928cc52bdd896baf9249d88b87a5f860))


### Documentation

* :memo: add configuration and deployment documentation ([eb6c275](https://github.com/stkr22/private-assistant-picture-display-skill-py/commit/eb6c2756cf89c717c662fd7ef6905af1a8a9b8c0)), closes [#5](https://github.com/stkr22/private-assistant-picture-display-skill-py/issues/5)
