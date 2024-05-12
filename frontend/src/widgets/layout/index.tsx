import { Header } from '@widgets/header';
import { Outlet } from 'react-router-dom';

import styles from './styles.module.css';

export const Layout = () => {
  return (
    <div className={styles.layout}>
      <Header />
      <main className={styles.container}>
        <Outlet />
      </main>
    </div>
  );
};
