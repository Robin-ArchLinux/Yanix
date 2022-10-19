import XMonad

import XMonad.Util.EZConfig
import XMonad.Util.Ungrab

myModMask             = mod4Mask                                :: KeyMask
myTerminal            = "alacritty"                             :: String
myBrowser             = "google-chrome-stable"                  :: String
myIDE                 = "emacsclient -c -a emacs"               :: String
myBorderWidth         = 2                                       :: Dimension
-- myFocusedBorderColor  = 

main :: IO ()
main = xmonad $ def
    { modMask       = myModMask,                   -- Rebind Mod to the Super key
      modTerminal   = myTerminal
    }