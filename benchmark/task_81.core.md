
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
length xs = lenAcc xs zero
```

# dependencies
## 0
```haskell
lenAcc :: [a] -> Int -> Int
```
## 1
```haskell
zero :: Num a => a
```
