# Evidence and pin policy

## Evidence order

1. Current top: port existence, direction, and module ownership.
2. Current target XDC: active LOC and IOSTANDARD.
3. Main-board schematic/PST: FPGA pin net, level conversion, zero-ohm or option resistor, assembly branch, and board connector.
4. Delay-board schematic: device instance, local interface, function label, and analog connector.
5. Cable table or continuity measurement: mapping between main-board logical groups and delay-board physical instances.

## Required result shape

For every asserted pin mapping, record:

- RTL top port;
- input/output direction;
- active LOC and IOSTANDARD;
- main-board FPGA-side net;
- intermediate resistor, level shifter, or multiplexed branch;
- external connector and pin;
- CW/GS assembly status;
- page/zone or PST source;
- evidence label;
- pending confirmation.

If any field is unavailable, say `未激活`, `未确认`, or `不适用`.

## Forbidden inference

- Device suffixes do not determine connector numbers.
- AD766 RTL group numbers do not determine schematic O numbers.
- G1/G2/G3 do not determine delay-board AD677 instance suffixes.
- A historical XDC does not determine a current FPGA pin.
- Zero duplicate LOC does not establish cable continuity or device identity.

## Historical AD677 two-channel baseline

The following candidate groups belong to the earlier AD677_IO_DDS_TOP two-logical-channel review. They are historical reference, not a current 05_CW_TEST_HY module/channel map. Resolve every active AD677 use, driver, timing and probe against the selected current RTL/XPR/LTX before applying any row.

| Group | CLK | CAL | SAMPLE | BUSY | SCLK | SDAT |
|---|---|---|---|---|---|---|
| G1 | AL39 | AK42 | AL36 | P35 | R34 | F24 |
| G2 | K38 | H39 | C40 | AR32 | AM33 | P36 |
| G3 | G39 | AJ42 | AH33 | N33 | R33 | N34 |

All are candidates only for that baseline. Do not activate a candidate group without cable or physical continuity evidence; do not constrain newer targets to two channels because this table has a historical two-channel context.
