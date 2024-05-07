<!--
 Copyright 2023 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 -->

# How to contribute

We'd love to accept your patches and contributions to this project.

## Before you begin

### Sign our Contributor License Agreement

Contributions to this project must be accompanied by a
[Contributor License Agreement](https://cla.developers.google.com/about) (CLA).
You (or your employer) retain the copyright to your contribution; this simply
gives us permission to use and redistribute your contributions as part of the
project.

If you or your current employer have already signed the Google CLA (even if it
was for a different project), you probably don't need to do it again.

Visit <https://cla.developers.google.com/> to see your current agreements or to
sign a new one.

### Review our community guidelines

This project follows
[Google's Open Source Community Guidelines](https://opensource.google/conduct/).

## Contribution process

### Main branch

Main branch must only contain fully tested and fully working code. Each commit corresponds to a bug fix, new feature, code refactor, etc.

### Versioning

This project uses Semantic Versioning (SemVer), which consists of three numbers separated by dots (e.g., MAJOR.MINOR.PATCH):
- MAJOR version is increased for incompatible API changes or output format changes.
- MINOR version is increased for backward-compatible new features.
- PATCH version is increased for backward-compatible bug fixes.

To keep track of versions, Git Tagging is used. Tag each release with the corresponding version number:
- **git tag -a v0.1.0 -m "Release version 0.1.0":** To create the tag.
- **git push main v0.1.0:** To push the tag.

Finally, maintain the CHANGELOG.md file to document changes for each version, following the principles of Keep a Changelog (https://keepachangelog.com/).


### Add changes

1. Create a new branch with an adequate. 
2. Development and testing of that change must occur in and only in that branch. 
3. Fully test ensuring that nothing is broken.
4. Add changes to CHANGELOG.md.
5. Merge into main with adequate commit name and description.
6. Tag the commit.

### Code reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.