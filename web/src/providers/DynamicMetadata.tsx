"use client";

import { useEffect, useMemo } from "react";
import { useSettingsContext } from "@/providers/SettingsProvider";

export default function DynamicMetadata() {
  const { enterpriseSettings } = useSettingsContext();

  useEffect(() => {
    const title = enterpriseSettings?.application_name || "Insight";
    if (document.title !== title) {
      document.title = title;
    }
  }, [enterpriseSettings]);

  // Cache-buster so the favicon re-fetches after an admin uploads a new logo.
  const cacheBuster = useMemo(
    () => Date.now(),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [enterpriseSettings]
  );

  const favicon = enterpriseSettings?.use_custom_logo
    ? `/api/enterprise-settings/logo?v=${cacheBuster}`
    : "/insight.svg";

  return (
    <>
      <link rel="icon" type="image/svg+xml" href={favicon} />
      <link rel="alternate icon" type="image/x-icon" href="/insight.ico" />
      <link rel="shortcut icon" href="/insight.ico" />
    </>
  );
}
