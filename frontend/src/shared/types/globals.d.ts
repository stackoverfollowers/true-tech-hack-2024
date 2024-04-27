declare module '*.svg' {
  const content: any;
  export default content;
}
declare module '*.png' {
  const value: any;
  export default value;
}
declare module '*.scss' {
  const content: Record<string, string>;
  export default content;
}

declare module '*.module.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}
