export const withAuth = (Component: React.FC) => {
  return () => {
    // const { user } = useAuth()
    // if (!user) {
    //   return <Redirect to="/auth" />
    // }
    return <Component />;
  };
};
