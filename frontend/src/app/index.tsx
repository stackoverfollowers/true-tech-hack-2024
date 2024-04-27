import './styles/index.css';
import { RouterProvider } from 'react-router-dom';
import { router } from '@shared/router';
import { QueryClientProvider } from '@tanstack/react-query';
import { WithTheme } from './providers/withTheme';
import { queryClient } from '@shared/query/queryClient';

export const App = () => {
  return (
    <WithTheme>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </WithTheme>
  );
};

export default App;
