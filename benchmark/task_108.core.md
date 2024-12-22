
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/OldList.hs--words

# poly_type
Monomorphic

# signature
```haskell
words :: String -> [String]
```   

# code
```haskell
words s =  case dropWhile isSpace s of
                  "" -> []
                  s' -> w : words s''
                    where (w, s'') = break isSpace s'
```

# dependencies
## 0
```haskell
break :: (a -> Bool) -> [a] -> ([a],[a])
```
## 1
```haskell
dropWhile :: (a -> Bool) -> [a] -> [a]
```
## 2
```haskell
isSpace :: Char -> Bool
```
## 3
```haskell
(:) :: a -> [a] -> [a]
```
## 4
```haskell
[] :: [a]
```
## 5
```haskell
"" :: String
```
