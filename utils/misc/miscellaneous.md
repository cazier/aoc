### Updating Annual Readmes

Using sed I can update the status with these commands, but it's kind of arbitrarily done at the moment.

```bash
        _cmd "sed -i -E 's/${DAY}  \| ✔️ (\s+)\|(\s+)  /${DAY}  | ✔️ \1| ✔️\2/g' ${README}"
        _cmd "sed -i -E 's/${DAY}  \|(\s+)  /${DAY}  | ✔️\1/g' ${README}"
        _cmd "sed -i -E 's/(Part One: \*\*)[0-9]+/\1${DAY}/g' ${README}"
        _cmd "sed -i -E 's/(Part Two: \*\*)[0-9]+/\1${DAY}/g' ${README}"
```
