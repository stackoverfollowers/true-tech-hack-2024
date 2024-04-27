import { useContext } from 'react';
import { useTheme } from '@mui/material/styles';
import { Box } from '@mui/material';
import { ThemeContext } from '@app/providers/withTheme';
import { Button } from '@ui/button';
import WbSunnyRoundedIcon from '@mui/icons-material/WbSunnyRounded';
import ModeNightRoundedIcon from '@mui/icons-material/ModeNightRounded';

export const ThemeSwitch = () => {
  const theme = useTheme();
  const mode = useContext(ThemeContext);

  return (
    <Box sx={{ maxWidth: '32px' }}>
      <Button
        variant="text"
        onClick={mode.toggle}
        size="small"
        aria-label="button to toggle theme"
        sx={{ minWidth: '32px', height: '32px', p: '4px' }}
      >
        {theme.palette.mode === 'dark' ? (
          <WbSunnyRoundedIcon fontSize="small" />
        ) : (
          <ModeNightRoundedIcon fontSize="small" />
        )}
      </Button>
    </Box>
  );
};
