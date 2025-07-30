# Changelog

## 0.1.1 (2025-06-11)

Full Changelog: [v0.1.0...v0.1.1](https://github.com/Artemis-xyz/artemis/compare/v0.1.0...v0.1.1)

### Features

* **api:** api update ([75982a4](https://github.com/Artemis-xyz/artemis/commit/75982a4c1412d3e293c5c8bc61141100fe731482))
* **api:** api update ([8317c3f](https://github.com/Artemis-xyz/artemis/commit/8317c3f21898f02cdafcef2e905aef4c3bf66a1d))
* **api:** api update ([55a14f5](https://github.com/Artemis-xyz/artemis/commit/55a14f52828c9514aec55b3d97647f34d72db542))
* **api:** api update ([8ad5fcf](https://github.com/Artemis-xyz/artemis/commit/8ad5fcfa233d04812f188ec821dcf175af2af43a))


### Bug Fixes

* **package:** support direct resource imports ([ffe1237](https://github.com/Artemis-xyz/artemis/commit/ffe1237f5d9ea243072a3f7108410a067a3ff48f))


### Chores

* **ci:** fix installation instructions ([83263db](https://github.com/Artemis-xyz/artemis/commit/83263dbc2470ddd9011ccc6cab9a381182e02867))
* **ci:** upload sdks to package manager ([23b127f](https://github.com/Artemis-xyz/artemis/commit/23b127f890fb6c03b0f6556ce7a83b749a9052b3))
* **docs:** grammar improvements ([5f1fb2e](https://github.com/Artemis-xyz/artemis/commit/5f1fb2e18a3ac45b97b9bc6f44069dd13e63c18d))
* **docs:** remove reference to rye shell ([1b2a446](https://github.com/Artemis-xyz/artemis/commit/1b2a446a4b9144f7eb1fb6bc7af8b80286257c4a))
* **internal:** avoid errors for isinstance checks on proxies ([f4ad11a](https://github.com/Artemis-xyz/artemis/commit/f4ad11aa97fb51e4fb511b776eedfb1405c80384))
* **internal:** codegen related update ([48d04db](https://github.com/Artemis-xyz/artemis/commit/48d04db44cad4c39667aafdc7e1a5baf44d6ca54))
* **internal:** codegen related update ([ae42929](https://github.com/Artemis-xyz/artemis/commit/ae42929147ad79880694635e152b4255ad65d3c8))

## 0.1.0 (2025-05-07)

Full Changelog: [v0.0.1...v0.1.0](https://github.com/Artemis-xyz/artemis/compare/v0.0.1...v0.1.0)

### Features

* **api:** api update ([552e44a](https://github.com/Artemis-xyz/artemis/commit/552e44a0e4083fcfbba9f77fb4638704243a108a))
* **api:** api update ([f170cf6](https://github.com/Artemis-xyz/artemis/commit/f170cf6e001c7a70e06cc4b83af5311244bc4c26))
* **api:** api update ([#10](https://github.com/Artemis-xyz/artemis/issues/10)) ([b3302ce](https://github.com/Artemis-xyz/artemis/commit/b3302ce2f858014e2530e96c27d6be9b2bfede88))
* **client:** allow passing `NotGiven` for body ([#7](https://github.com/Artemis-xyz/artemis/issues/7)) ([9b87cc4](https://github.com/Artemis-xyz/artemis/commit/9b87cc4edaeafd3591dbfccba52b6a2f91f40f60))


### Bug Fixes

* **ci:** ensure pip is always available ([#20](https://github.com/Artemis-xyz/artemis/issues/20)) ([b06bd19](https://github.com/Artemis-xyz/artemis/commit/b06bd19791c64eac364765570bceacaa5705187c))
* **ci:** remove publishing patch ([#21](https://github.com/Artemis-xyz/artemis/issues/21)) ([86a370f](https://github.com/Artemis-xyz/artemis/commit/86a370fae92d86a4f3d4a5ce8ff9332285de6997))
* **client:** mark some request bodies as optional ([9b87cc4](https://github.com/Artemis-xyz/artemis/commit/9b87cc4edaeafd3591dbfccba52b6a2f91f40f60))
* **perf:** optimize some hot paths ([c68f63f](https://github.com/Artemis-xyz/artemis/commit/c68f63fbc5a649bbbdbe1718c2459c0162ccd690))
* **perf:** skip traversing types for NotGiven values ([9283aa4](https://github.com/Artemis-xyz/artemis/commit/9283aa4a013cdf8d118cce1f21799ba4b30a1530))
* **types:** handle more discriminated union shapes ([#19](https://github.com/Artemis-xyz/artemis/issues/19)) ([5bbda52](https://github.com/Artemis-xyz/artemis/commit/5bbda52b4f7275d1dc772da34aa86e248b0c5578))


### Chores

* **client:** minor internal fixes ([425301a](https://github.com/Artemis-xyz/artemis/commit/425301a86df604dd7c0253c5a7128396fad1a868))
* **docs:** update client docstring ([#13](https://github.com/Artemis-xyz/artemis/issues/13)) ([75a4929](https://github.com/Artemis-xyz/artemis/commit/75a4929d0925652e550f5d3d11bf1775f6fb9f80))
* fix typos ([#22](https://github.com/Artemis-xyz/artemis/issues/22)) ([b1e7c2d](https://github.com/Artemis-xyz/artemis/commit/b1e7c2df29588905c05d600ff09a2cba5e9f1d76))
* **internal:** base client updates ([4f43cc1](https://github.com/Artemis-xyz/artemis/commit/4f43cc173b3a14df2a3605738bcd007d5bd41885))
* **internal:** bump pyright version ([a4f15f2](https://github.com/Artemis-xyz/artemis/commit/a4f15f2b9eb5bee85f9d683dabac55cf956ab467))
* **internal:** bump rye to 0.44.0 ([#18](https://github.com/Artemis-xyz/artemis/issues/18)) ([e28b4f7](https://github.com/Artemis-xyz/artemis/commit/e28b4f764df3ce9229ab258903ee51e83ac32566))
* **internal:** codegen related update ([#17](https://github.com/Artemis-xyz/artemis/issues/17)) ([979b2e8](https://github.com/Artemis-xyz/artemis/commit/979b2e8262687e676103c5d09b7e81976047a825))
* **internal:** expand CI branch coverage ([5300422](https://github.com/Artemis-xyz/artemis/commit/53004222e98c194a924c9aefadd4a9da06ea56f3))
* **internal:** fix devcontainers setup ([#9](https://github.com/Artemis-xyz/artemis/issues/9)) ([60ecc64](https://github.com/Artemis-xyz/artemis/commit/60ecc6486b6589c7e54720a6c5be08f7f1d094e4))
* **internal:** properly set __pydantic_private__ ([#11](https://github.com/Artemis-xyz/artemis/issues/11)) ([e6b9478](https://github.com/Artemis-xyz/artemis/commit/e6b94784244428625ebc8de81f89f049b0aba0c1))
* **internal:** reduce CI branch coverage ([1997764](https://github.com/Artemis-xyz/artemis/commit/199776496a104512554039facd2ac657b65b574b))
* **internal:** remove extra empty newlines ([#16](https://github.com/Artemis-xyz/artemis/issues/16)) ([f104ff7](https://github.com/Artemis-xyz/artemis/commit/f104ff79edad01208fb5387f86456c574262250b))
* **internal:** remove trailing character ([#23](https://github.com/Artemis-xyz/artemis/issues/23)) ([443fbcb](https://github.com/Artemis-xyz/artemis/commit/443fbcb12d5ebde2e12b932991980a003860c095))
* **internal:** remove unused http client options forwarding ([#14](https://github.com/Artemis-xyz/artemis/issues/14)) ([4fdf048](https://github.com/Artemis-xyz/artemis/commit/4fdf048bee3392cbcf16bf504baba158caddf61e))
* **internal:** slight transform perf improvement ([#24](https://github.com/Artemis-xyz/artemis/issues/24)) ([971eaf2](https://github.com/Artemis-xyz/artemis/commit/971eaf2a506c9bf9e066d804b6ff9e590aa0578b))
* **internal:** update models test ([d1b4be5](https://github.com/Artemis-xyz/artemis/commit/d1b4be54b49f7cf1cc1c2e3c9b2faa030b9bb3a8))
* **internal:** update pyright settings ([d8f7cf3](https://github.com/Artemis-xyz/artemis/commit/d8f7cf35c7e3a4360eefb1f97cf829145add31a4))


### Documentation

* update URLs from stainlessapi.com to stainless.com ([#12](https://github.com/Artemis-xyz/artemis/issues/12)) ([0d123ef](https://github.com/Artemis-xyz/artemis/commit/0d123efb40635365e50847f4011c7efe6d10eb39))

## 0.0.1 (2025-02-20)

Full Changelog: [v0.0.1-alpha.0...v0.0.1](https://github.com/Artemis-xyz/artemis/compare/v0.0.1-alpha.0...v0.0.1)

### Chores

* go live ([#3](https://github.com/Artemis-xyz/artemis/issues/3)) ([cd2bb12](https://github.com/Artemis-xyz/artemis/commit/cd2bb129e07fd484bb1af650db44ad9dc1cc4a4a))
* sync repo ([018633f](https://github.com/Artemis-xyz/artemis/commit/018633f7495103403e8504e87204e189012719e1))
* update SDK settings ([#5](https://github.com/Artemis-xyz/artemis/issues/5)) ([e04c2ab](https://github.com/Artemis-xyz/artemis/commit/e04c2ab30fdeb63fd14824aebd67a2054957b430))
