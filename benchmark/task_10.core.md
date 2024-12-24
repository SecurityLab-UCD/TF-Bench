
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--enumFrom

# poly_type
Ad-hoc

# signature
```haskell
enumFrom :: Enum a => a -> [a]
```   

# code
```haskell
enumFrom x = map toEnum [fromEnum x ..]
```

# dependencies
## 0
```haskell
map :: (a -> b) -> [a] -> [b]
```
## 1
```haskell
toEnum :: Enum a => Int -> a
```
## 2
```haskell
fromEnum :: Enum => a -> Int
```
