doc: |
  CDR Parser for Tetra switch software v7.0
meta:
  id: tetra
  file-extension: cdr
  endian: le
  
  imports:
    - bcd
seq:
  - id: block
    type: block
    size: 65408
    repeat: eos
types:
  block:
    seq:  
      - id: header
        type: header
      - id: events
        type: events
        size: header.length-65
      - id: trailer
        type: trailer
  event:
    seq:
      - id: len_rec
        type: u2
      - id: body
        size: len_rec-2
        type:
          switch-on: len_rec
          cases:
            271: toc
            133: tcc
            113: in_g
            99: out_g
            125: fraw
            262: sds
            141: pd
            97: reg
  header:
    seq:
      - id: magic
        contents: [0x29, 0x00, 0x00]
      - id: size
        contents: [0x08]
      - id: type
        contents: [0x01, 0x00]
      - id: length
        type: u2
      - id: exchange_id
        size: 10
      - id: first_record
        type: u4
      - id: batch_num
        type: u4
      - id: block_num
        type: u2
      - id: start_time
        size: 7
      - id: version
        size: 6
  events:
    seq:
      - id: event
        type: event
        repeat: eos
  toc:
    seq:
      - id: type
        type: u1
        enum: types
      - id: version
        type: u1
      - id: dxt_id
        size: 4
      - id: checksum
        type: u2
      - id: seq_num
        type: u2
      - id: unused
        size: 6
      - id: call_reference
        type: u4
      - id: served_number
        size: 10
      - id: served_nitsi
        size: 10
      - id: organization_block
        size: 12
      - id: called_number
        size: 14
      - id: translated_number
        size: 14
      - id: translated_nitsi
        size: 10
      - id: connected_number
        size: 14
      - id: connected_nitsi
        size: 10
      - id: connection_group
        size: 2
      - id: connected_dxt
        size: 4
      - id: served_dxt
        size: 4
      - id: location
        type: u2
      - id: cell_identity
        size: 1
      - id: basic_service_used
        size: 4
      - id: basic_servise_request
        size: 4
      - id: priority
        size: 1
      - id: urgency_class
        size: 1
      - id: queuing_priority
        size: 1
      - id: duplex
        size: 1
      - id: hook
        size: 1
      - id: encryption
        size: 1
      - id: members
        type: u2
      - id: allocations
        size: 2
      - id: channel_usage_time
        size: 4
      - id: number_of_groups
        size: 1
      - id: list_of_groups
        size: 80
      - id: setup_time
        size: 8
        type: time
      - id: answer_time
        size: 8
        type: time
      - id: connected_time
        size: 8
        type: time
      - id: release_time
        size: 8
        type: time
      - id: duration
        type: u4
      - id: termination
        type: u1
        enum: terminations
      - id: diagnostic
        size: 2
  tcc:
    seq:
      - id: type
        type: u1
        enum: types
      - id: version 
        size: 1
      - id: dxt
        size: 4
      - id: checksum
        size: 2
      - id: seq_num
        type: u2
      - id: skeep
        size: 5
      - id: call_reference
        type: u4
      - id: served_number
        size: 10
      - id: served_nitsi
        size: 10
      - id: organisation_block
        size: 12
      - id: calling_number
        size: 14
      - id: calling_nitsi
        size: 10
      - id: dxt_id
        size: 4
      - id: location
        type: u2
      - id: call_identity
        size: 1
      - id: service
        size: 4
      - id: priority
        size: 1
      - id: urgency
        size: 1
      - id: queuie
        size: 1
      - id: duplex
        size: 1
      - id: hook
        size: 1
      - id: encription
        size: 1
      - id: setup_time
        size: 8
        type: time
      - id: answer_time
        size: 8
        type: time
      - id: connected_time
        size: 8
        type: time
      - id: release_time
        size: 8
        type: time
      - id: duration
        type: u4
      - id: termination
        type: u1
        enum: terminations
      - id: diagnoistic
        size: 2
        
  in_g:
    seq:
      - id: type
        type: u1
        enum: types
      - id: version
        type: u1
      - id: dxt1
        type: u4
      - id: checksum
        type: u2
      - id: seq_num
        type: u2
      - id: call_reference
        type: u4
      - id: calling_number
        size: 14
      - id: called_number
        size: 10
      - id: translated_number
        size: 14
      - id: translated_ntsi
        size: 10
      - id: dxt
        type: u4
      - id: inc_int
        size: 6
      - id: conn_group
        type: u2
      - id: mni
        type: u4
      - id: pulse
        type: u2
      - id: setup_time
        size: 8
        type: time
      - id: answer_time
        size: 8
        type: time
      - id: release_time
        size: 8
        type: time
      - id: duration
        type: u4
      - id: termination
        type: u1
        enum: terminations
      - id: diagnoistic
        size: 2

  out_g:
    seq:
      - id: type
        type: u1
        enum: types
      - id: version
        type: u1
      - id: identity
        type: u4
      - id: checksum
        type: u2
      - id: seq_number
        type: u2
      - id: call_reference
        type: u4
      - id: calling_number
        size: 10
      - id: calling_ntsi
        size: 10
      - id: transmitted_number
        size: 14
      - id: dxt
        size: 4
      - id: out_int
        size: 6
      - id: conn_group
        size: 2
      - id: mni
        size: 4
      - id: setup_time
        size: 8
        type: time
      - id: answer_time
        size: 8
        type: time
      - id: release_time
        size: 8
        type: time
      - id: duration
        type: u4
      - id: pulses_pstn
        size: 2
      - id: termination
        type: u1
        enum: terminations
      - id: diagnoistic
        size: 2

  fraw:
    seq:
      - id: body
        size: 125-2
  sds:
    seq:
      - id: body
        size: 262-2
  pd:
    seq:
      - id: body
        size: 141-2
  reg:
    seq:
    - id: type
      type: u1
      enum: types
    - id: version
      type: u1
    - id: dxt
      type: u4
    - id: checksum
      type: u2
    - id: seq_num
      type: u2
    - id: served_nitsi
      size: 10
    - id: assigned_itsi
      size: 10
    - id: originator_itsi
      size: 10
    - id: organisation_block
      size: 12
    - id: tei
      size: 8
    - id: registration_type
      size: 1
    - id: authentication
      size: 1
    - id: encription
      size: 1
    - id: class_ms
      size: 4
    - id: subscriber_class
      size: 2
    - id: dxt_id
      size: 4
    - id: prev_dxt_id
      size: 4
    - id: location
      type: u2
    - id: prev_location
      type: u2
    - id: cell
      size: 1
    - id: channel
      size: 1
    - id: timestamp
      type: time
      size: 8
    - id: accept
      size: 1
    - id: reject
      size: 1
    - id: diagnostic
      size: 2

  trailer:
    seq:
      - id: body
        size: 24

  time:
    seq:
      - id: msec
        type: bcd(2, 4, false)
      - id: sec
        type: bcd(2, 4, false)
      - id: min
        type: bcd(2, 4, false)
      - id: hour
        type: bcd(2, 4, false)
      - id: day
        type: bcd(2, 4, false)
      - id: month
        type: bcd(2, 4, false)
      - id: year
        type: bcd(2, 4, false)
      - id: age
        type: bcd(2, 4, false)
    instances:
      full_year:
        value: age.as_int*100 + year.as_int

enums:
  terminations:
    1: ok
    2: busy
    3: partial_record
    4: bad_number
    5: reject_by_user
    6: reject_by_operator
    7: reject_by_gw
    8: eight
    9: faill
  types:
    1: toc
    2: tcc
    3: in_g
    4: out_g
    5: redirect
    6: sms
    7: farward
    8: data
    9: reg