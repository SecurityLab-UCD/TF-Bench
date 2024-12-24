
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Text/Read.hs--read

# poly_type
Ad-hoc

# signature
```haskell
read :: Read a => String -> a
```   

# code
```haskell
read s = either errorWithoutStackTrace id (readEither s)
```

# dependencies
## 0
```haskell
either :: (a -> c) -> (b -> c) -> Either a b -> c
```
## 1
```haskell
readEither :: Read a => String -> Either String a
```
## 2
```haskell
id :: a -> a
```
## 3
```haskell
errorWithoutStackTrace :: String -> a
```