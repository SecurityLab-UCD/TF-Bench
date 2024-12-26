
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Show.hs--show

# poly_type
Ad-hoc

# signature
```haskell
show :: Show a => a -> String
```   

# code
```haskell
show x = shows x emptyStr
```

# dependencies
## 0
```haskell
shows :: (Show a) => a -> ShowS
```
## 1
```haskell
type ShowS = String -> String
```
## 2
```haskell
emptyStr :: String
```