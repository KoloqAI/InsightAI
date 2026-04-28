import type { IconProps } from "@opal/types";

const SvgOnyxTyped = ({ size, ...props }: IconProps) => (
  <svg
    height={size}
    viewBox="0 0 152 64"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <text
      x="0"
      y="46"
      fontFamily="var(--font-hanken-grotesk), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
      fontSize="44"
      fontWeight="700"
      letterSpacing="-1"
      fill="var(--theme-primary-05)"
    >
      Insight
    </text>
  </svg>
);

export default SvgOnyxTyped;
