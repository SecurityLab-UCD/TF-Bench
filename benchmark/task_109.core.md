
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/OldList.hs--unwords

# poly_type
Monomorphic

# signature
```haskell
unwords :: [String] -> String
```   

# code
```haskell
unwords [] =  emptyStr
unwords ws =  foldr1 (\w s -> w ++ space:s) ws
```

# dependencies
## 0
```haskell
(++) :: [a] -> [a] -> [a]
```
## 1
```haskell
foldr1 :: Foldable t => (a -> a -> a) -> t a -> a
```
## 2
```haskell
space :: Char
```
## 3
```haskell
emptyStr :: String
```