
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--length

# poly_type
Parametric

# signature
```haskell
length :: [a] -> Int
```   

# code
```haskell
length xs = lenAcc xs 0
```

# dependencies
## 0
```haskell
lenAcc :: [a] -> Int -> Int
```
