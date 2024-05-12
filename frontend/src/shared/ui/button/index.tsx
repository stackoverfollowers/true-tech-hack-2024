import { forwardRef } from 'react';
import { Link } from 'react-router-dom';
import { Button as MuiButton } from '@mui/material';
import { ButtonProps } from '@mui/material';

export const Button = forwardRef<Ref, Props>((props: Props, ref) => {
  if (props.href) {
    return (
      <Link to={props.href}>
        <MuiButton ref={ref} {...props} />
      </Link>
    );
  }

  return <MuiButton component={Link} ref={ref} {...props} />;
});

type Ref = HTMLButtonElement;

type Props = ButtonProps & {
  href?: string;
};
