import CssBaseline from '@mui/material/CssBaseline';
import { createContext, useMemo, useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { createTheme } from '@mui/material';

export const ThemeContext = createContext({ toggle: () => { } });

export const WithTheme = ({ children }: Props) => {
  const [mode, setMode] = useState<'light' | 'dark'>('light');
  const colorMode = useMemo(
    () => ({
      toggle: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    [],
  );

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
        },
      }),
    [mode],
  );

  return (
    <ThemeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
};

type Props = {
  children: React.ReactNode;
};
