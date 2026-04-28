"use client";

import {
  SvgBracketCurly,
  SvgGlobe,
  SvgLinkedDots,
  SvgMcp,
  SvgMicrophone,
  SvgNetworkGraph,
  SvgPaintBrush,
  SvgSparkle,
} from "@opal/icons";
import type { IconFunctionComponent } from "@opal/types";
import Text from "@/refresh-components/texts/Text";
import { cn } from "@/lib/utils";

interface FeatureChip {
  Icon: IconFunctionComponent;
  label: string;
  position: string;
  delaySeconds: number;
}

const FEATURE_CHIPS: FeatureChip[] = [
  {
    Icon: SvgSparkle,
    label: "Agentic RAG",
    position: "top-[12%] left-[6%]",
    delaySeconds: 0,
  },
  {
    Icon: SvgNetworkGraph,
    label: "Deep Research",
    position: "top-[26%] left-[20%]",
    delaySeconds: 1.1,
  },
  {
    Icon: SvgGlobe,
    label: "Web Search",
    position: "top-[64%] left-[5%]",
    delaySeconds: 2.4,
  },
  {
    Icon: SvgPaintBrush,
    label: "Image Generation",
    position: "bottom-[14%] left-[20%]",
    delaySeconds: 3.6,
  },
  {
    Icon: SvgMcp,
    label: "Actions & MCP",
    position: "top-[14%] right-[6%]",
    delaySeconds: 0.6,
  },
  {
    Icon: SvgBracketCurly,
    label: "Code Execution",
    position: "top-[30%] right-[20%]",
    delaySeconds: 1.7,
  },
  {
    Icon: SvgMicrophone,
    label: "Voice Mode",
    position: "top-[66%] right-[5%]",
    delaySeconds: 2.9,
  },
  {
    Icon: SvgLinkedDots,
    label: "50+ Connectors",
    position: "bottom-[14%] right-[20%]",
    delaySeconds: 4.1,
  },
];

export default function AuthShowcase() {
  return (
    <div
      aria-hidden="true"
      className="absolute inset-0 overflow-hidden pointer-events-none"
    >
      {/* Soft brand-glow blobs */}
      <div
        className={cn(
          "absolute -top-40 -left-32 w-[36rem] h-[36rem] rounded-full",
          "bg-theme-blue-05 opacity-40 blur-[120px]"
        )}
      />
      <div
        className={cn(
          "absolute -bottom-48 -right-40 w-[40rem] h-[40rem] rounded-full",
          "bg-theme-primary-05 opacity-20 blur-[120px]"
        )}
      />
      <div
        className={cn(
          "absolute top-[28%] right-[15%] w-[24rem] h-[24rem] rounded-full",
          "bg-theme-blue-02 opacity-30 blur-[100px]"
        )}
      />

      {/* Dot grid texture, masked to a soft elliptical fade */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage:
            "radial-gradient(var(--border-02) 1px, transparent 1px)",
          backgroundSize: "24px 24px",
          maskImage:
            "radial-gradient(ellipse at center, #000 25%, transparent 75%)",
          WebkitMaskImage:
            "radial-gradient(ellipse at center, #000 25%, transparent 75%)",
        }}
      />

      {/* Floating feature chips — desktop only, hidden on mobile to keep card focal */}
      <div className="hidden md:block absolute inset-0">
        {FEATURE_CHIPS.map(({ Icon, label, position, delaySeconds }) => (
          <div
            key={label}
            className={cn(
              "absolute inline-flex items-center gap-2 px-3 py-1.5",
              "rounded-full border border-border-01",
              "backdrop-blur-md shadow-00",
              "animate-auth-chip-float motion-reduce:animate-none",
              position
            )}
            style={{
              backgroundColor:
                "color-mix(in srgb, var(--background-tint-00) 60%, transparent)",
              animationDelay: `${delaySeconds}s`,
            }}
          >
            <Icon
              size={14}
              className="text-action-link-05 flex-shrink-0"
            />
            <Text secondaryAction text05 nowrap>
              {label}
            </Text>
          </div>
        ))}
      </div>
    </div>
  );
}
