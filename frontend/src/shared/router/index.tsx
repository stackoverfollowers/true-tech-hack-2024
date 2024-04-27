import { createBrowserRouter } from 'react-router-dom';
import { SettingsPage } from '../../pages/settings';
import { AuthPage } from '../../pages/auth';
import { ProfilePage } from '../../pages/profile';
import { RootPage } from '../../pages/root';
import { Layout } from '@widgets/layout';

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: '/',
        element: <RootPage />,
      },
      {
        path: '/auth',
        element: <AuthPage />,
      },
      {
        path: '/profile',
        element: <ProfilePage />,
      },
      {
        path: '/settings',
        element: <SettingsPage />,
      },
    ],
  },
]);
