
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/OldList.hs--lines

# poly_type
Monomorphic

# signature
```haskell
lines :: String -> [String]
```   

# code
```haskell
lines emptyStr =  []
lines s  =  cons (case break (== newLine) s of
       (l, s') -> (l, case s' of
                       []      -> []
                       _:s''   -> lines s''))
  where
    cons ~(h, t) =  h : t
```

# dependencies
## 0
```haskell
break :: (a -> Bool) -> [a] -> ([a],[a])
```
## 1
```haskell
emptyStr :: String
```
## 2
```haskell
newLine :: Char
```
## 3
```haskell
(==) :: Eq a => a -> a -> Bool
```
