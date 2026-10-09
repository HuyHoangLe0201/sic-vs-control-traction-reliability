# P1-1: separate vs superposed rainflow counting (fvdr, most damaged chip under separate counting)

| config | policy | rule | chip | D separate | D superposed | ratio |
|---|---|---|---|---|---|---|
| Si-NPC | base | ton_clip | D6 / D5 | 1.3e-05 | 1.54e-05 | 1.187 |
| Si-NPC | base | ton_free | D5 / D5 | 3.88e-06 | 6.72e-06 | 1.730 |
| Si-NPC | har | ton_clip | D1 / D1 | 1.14e-06 | 1.34e-06 | 1.183 |
| Si-NPC | har | ton_free | D1 / D1 | 5.45e-07 | 7.6e-07 | 1.393 |
| Si-ANPC | base | ton_clip | D6 / D6 | 1.11e-05 | 1.31e-05 | 1.176 |
| Si-ANPC | base | ton_free | D5 / D6 | 3.37e-06 | 5.7e-06 | 1.692 |
| Si-ANPC | har | ton_clip | D3 / D3 | 8.7e-07 | 1.02e-06 | 1.169 |
| Si-ANPC | har | ton_free | D3 / D3 | 4.18e-07 | 5.67e-07 | 1.357 |
| SiC-ANPC | base | ton_clip | S2 / S2 | 9.99e-07 | 1.02e-06 | 1.020 |
| SiC-ANPC | base | ton_free | S2 / S3 | 1.6e-07 | 1.92e-07 | 1.194 |
| SiC-ANPC | har | ton_clip | S2 / S2 | 2.53e-07 | 2.64e-07 | 1.040 |
| SiC-ANPC | har | ton_free | S2 / S3 | 3.45e-08 | 4.68e-08 | 1.358 |

| rule | counting | kappa sub vs Si-NPC+har | kappa sub vs Si-ANPC+har | both vs Si-ANPC |
|---|---|---|---|---|
| ton_clip | separate | 0.88 | 1.15 | 0.291 |
| ton_clip | superposed | 0.759 | 1 | 0.259 |
| ton_free | separate | 0.294 | 0.384 | 0.0825 |
| ton_free | superposed | 0.252 | 0.338 | 0.0825 |
