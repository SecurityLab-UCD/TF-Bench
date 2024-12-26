
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--lookup

# poly_type
Ad-hoc

# signature
```haskell
lookup :: (Eq a) => a -> [(a,b)] -> Maybe b
```   

# code
```haskell
lookup _key []          =  Nothing
lookup  key ((x,y):xys)
    | key == x           =  Just y
    | otherwise         =  lookup key xys
```

# dependencies
## 0
```haskell
data Maybe a = Nothing | Just a
```
## 1
```haskell
(==) :: Eq a => a -> a -> Bool
```
