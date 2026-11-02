"""VIR-F20T5-CR1: passive native-action tracker and one staged context rebuild.

Default OFF. No environment operation or model request is initiated here.
"""
from __future__ import annotations
import copy, hashlib, json, math, os
from dataclasses import dataclass
from pathlib import Path

CONDITION = 'K1VIR-F20T5-CR1'
K1 = 'K1_RESPONSE_RECOVERY'
VIR = 'VIR_VISIBLE_IMMOBILITY'
ADAPTER_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

def grid_hash(grid):
    return hashlib.sha256(json.dumps(grid,separators=(',',':')).encode()).hexdigest()

@dataclass
class Tracker:
    key: str
    ordinal: int
    elapsed: float
    level: int
    game_id: str | None = None
    count: int = 0
    anchor: float = 0.0
    epoch: int = 0
    pending: dict | None = None
    attempted: bool = False

class VIRMixin:
    def _vir_initialize(self):
        self._vir_enabled = os.environ.get('LOCAL_ANALYZER_VIR_ENABLED','0').lower() in ('1','true')
        if self._stagnation_recovery_threshold not in (0,1):
            raise ValueError('Combined candidate accepts response K=0 or K=1 only')
        self._combined_enabled=self._vir_enabled or self._stagnation_recovery_threshold==1
        self._combined_reset()
        self._vir_tracker = None
        self._vir_applied = None
        self._vir_event_sequence = 0
        self._vir_event_counts = {}
        self._vir_write_errors = 0
        self._vir_finalized = False
        if self._combined_enabled:
            self._study2_arm = CONDITION

    def _vir_emit(self,event,**fields):
        try:
            self._vir_event_sequence += 1
            self._vir_event_counts[event]=self._vir_event_counts.get(event,0)+1
            mechanism=fields.pop('mechanism',VIR)
            counts=self._mechanism_counts.setdefault(mechanism,{})
            counts[event]=counts.get(event,0)+1
            t=self._vir_tracker
            row={'schema':'combined-recovery-v1','condition':CONDITION,'adapter_sha256':ADAPTER_SHA256,
                 'mechanism':mechanism,'applied_context_order':list(self._recovery_order),'attempt_order':list(self._attempt_order),
                 'event':event,'sequence':self._vir_event_sequence,'turn_sequence':getattr(self,'_study2_turn_sequence',None),
                 'game_key':t.key,'game_id':t.game_id,'action_ordinal':t.ordinal,'elapsed_s':t.elapsed,
                 'level':t.level,'epoch':t.epoch,'guard_used':self._stagnation_recovery_used if mechanism==K1 else t.attempted,
                 'K1_guard_used':self._stagnation_recovery_used,'VIR_guard_used':t.attempted,
                 'event_counts':dict(self._vir_event_counts),'write_errors_before':self._vir_write_errors,**fields}
            path=Path(t.key);log=path.with_name(path.stem+'_combined_recovery_events.jsonl')
            with log.open('a',encoding='utf-8') as f:f.write(json.dumps(row,separators=(',',':'))+'\n')
            summary=path.with_name(path.stem+'_combined_recovery_summary.json')
            temporary=summary.with_name(summary.name+'.tmp')
            temporary.write_text(json.dumps(self.vir_summary(),separators=(',',':'))+'\n',encoding='utf-8')
            temporary.replace(summary)
        except Exception:
            self._vir_write_errors += 1

    def vir_summary(self):
        return {'condition':CONDITION,'adapter_sha256':ADAPTER_SHA256,'enabled':self._combined_enabled,'VIR_enabled':self._vir_enabled,'K1_enabled':self._stagnation_recovery_threshold==1,
                'game_key':self._vir_tracker.key if self._vir_tracker else None,
                'game_id':self._vir_tracker.game_id if self._vir_tracker else None,
                'response_recovery_k':self._stagnation_recovery_threshold,
                'mechanism_counts':copy.deepcopy(self._mechanism_counts),'applied_context_order':list(self._recovery_order),'attempt_order':list(self._attempt_order),
                'K1_attempt_used':self._stagnation_recovery_used,
                'VIR_attempt_used':bool(self._vir_tracker and self._vir_tracker.attempted),
                'any_context_applied':bool(self._recovery_order),
                'event_counts':dict(self._vir_event_counts),'write_errors':self._vir_write_errors,
                'finalized':self._vir_finalized,
                'attempt_used':bool(self._stagnation_recovery_used or (self._vir_tracker and self._vir_tracker.attempted))}

    def vir_finalize(self,**fields):
        """Return the final in-memory receipt even when sidecar writes fail."""
        if not self._combined_enabled or self._vir_tracker is None:return None
        if not self._vir_finalized:
            self._vir_finalized=True
            self._vir_emit('game_end',mechanism='COMBINED',**fields)
        return self.vir_summary()

    def vir_seed(self,state_path,ordinal,elapsed,level,game_id=None):
        if not self._combined_enabled:return
        try:
            key=str(Path(state_path).resolve())
            if self._vir_tracker is None or self._vir_tracker.key!=key:
                self._vir_tracker=Tracker(key,int(ordinal),float(elapsed),int(level),game_id=game_id,anchor=float(elapsed))
                self._vir_applied=None
                self._combined_reset()
                self._stagnation_recovery_used=False;self._no_tool_streak=0
                self._vir_event_sequence=0;self._vir_event_counts={};self._vir_write_errors=0
                self._vir_finalized=False
                self._vir_emit('game_start',response_recovery_k=self._stagnation_recovery_threshold,mechanism='COMBINED')
        except Exception:
            self._vir_tracker=None

    def _vir_break(self,reason):
        t=self._vir_tracker
        if t.pending:self._vir_emit('expired',eligibility_id=t.pending['id'],reason=reason)
        t.pending=None;t.count=0;t.anchor=t.elapsed;t.epoch+=1

    def vir_observe(self,state_path,payload,grid):
        if not self._combined_enabled:return
        try:
            t=self._vir_tracker
            if t is None or t.key!=str(Path(state_path).resolve()):return
            o=int(payload['action_num']);now=float(payload['run_elapsed_seconds'])
            if o<=t.ordinal:return  # native cursor: no history replay double-counting
            self._k1_invalidate('environment_action')
            previous=t.elapsed;gap=o!=t.ordinal+1
            t.ordinal=o;t.elapsed=now;t.level=int(payload['level'])
            valid=(math.isfinite(now) and now>=previous and
                   isinstance(payload.get('board_changed'),bool) and
                   all(isinstance(payload.get(k),bool) for k in ('done','game_over','run_complete','level_completed')))
            reason=('gap' if gap else 'invalid_observation' if not valid else
                    'terminal' if payload['state']!='NOT_FINISHED' or any(payload[k] for k in ('done','game_over','run_complete')) else
                    'RESET' if str(payload.get('action_display','')).startswith('RESET') else
                    'level_completed' if payload['level_completed'] else
                    'visible_change' if payload['board_changed'] else None)
            if reason:self._vir_break(reason)
            else:
                if t.count==0:t.anchor=previous
                t.count+=1
                if self._vir_enabled and t.count>=20 and now-t.anchor>=300 and t.pending is None and not t.attempted:
                    e={'id':f'{CONDITION}:{t.ordinal}:{t.epoch}','first_action':o-t.count+1,
                       'eligible_action':o,'epoch':t.epoch,'level':t.level,'frame_sha256':grid_hash(grid)}
                    t.pending=e
                    self._vir_emit('eligible',eligibility_id=e['id'],count=t.count,span_s=now-t.anchor,
                                   first_action=e['first_action'],frame_sha256=e['frame_sha256'])
            for applied in self._recovery_applications:
                if applied.get('response_received') and not applied.get('action_observed'):
                    applied['action_observed']=True
                    self._vir_emit('next_environment_action',mechanism=applied['mechanism'],attempt_id=applied['id'],
                        request_id=applied.get('request_id'),action_display=payload.get('action_display'),
                        board_changed=payload.get('board_changed'),level_completed=payload.get('level_completed'))
            if self._recovery_applications:
                self._vir_emit('environment_observation',mechanism='COMBINED',
                    action_display=payload.get('action_display'),board_changed=payload.get('board_changed'),
                    level_completed=payload.get('level_completed'),done=payload.get('done'),
                    game_over=payload.get('game_over'),run_complete=payload.get('run_complete'))
        except Exception:
            if self._vir_tracker is not None:self._vir_break('observer_error')

    def _vir_prepare_entry(self,state_path,action_num,current_frame,history_entries,valid_actions,should_stop):
        if not self._vir_enabled:return None
        t=self._vir_tracker
        if t is None or not t.pending or t.attempted:return None
        if should_stop is not None:
            try:
                if should_stop():
                    self._vir_emit('deferred',reason='existing_stop',eligibility_id=t.pending['id']);return None
            except Exception:
                self._vir_emit('deferred',reason='stop_check_error',eligibility_id=t.pending['id']);return None
        p=t.pending
        try:
            valid=(str(Path(state_path).resolve())==t.key and int(action_num)==t.ordinal and
                   current_frame is not None and int(current_frame.step)==t.ordinal and
                   int(current_frame.level)==t.level==p['level'] and t.epoch==p['epoch'] and
                   t.count>=20 and t.elapsed-t.anchor>=300 and grid_hash(current_frame.grid)==p['frame_sha256'])
        except Exception:valid=False
        if not valid:self._vir_break('entry_revalidation');return None
        t.attempted=True;self._recovery_boundary_used=True;attempt_id=p['id']+':attempt'
        self._combined_record_attempt(VIR,attempt_id)
        self._vir_emit('attempt',attempt_id=attempt_id,eligibility_id=p['id'],count=t.count,
                       span_s=t.elapsed-t.anchor,frame_sha256=p['frame_sha256'])
        try:
            # Only the candidate receives mutable context copies. Build/trim
            # exceptions cannot clear or alter the live history and hypotheses.
            candidate=copy.copy(self)
            candidate._history_messages=copy.deepcopy(self._history_messages)
            candidate._summarized_knowledge=copy.deepcopy(self._summarized_knowledge)
            candidate._summarized_knowledge['current_plan']=''
            prompt=candidate._build_user_prompt(action_num,valid_actions=valid_actions,
                current_frame=current_frame,history_entries=history_entries,previous_step_summary=self._last_step_summary)
            prompt+=('\n\nVisible-immobility recovery: the last '+str(t.count)+
                ' executed environment actions within this level produced no change in the full visible grid over '+
                f'{t.elapsed-t.anchor:.1f}'+' seconds. The previous conversational plan is discarded. '
                'Re-ground from the current frame, runtime history, valid actions and latest action result. '
                'Retained notes may be stale; verify them against current evidence. Use Python to inspect '
                'the evidence before selecting the next valid action and form a revised plan.')
            messages=candidate._trim_messages_for_context([
                {'role':'system','content':self._system_prompt},candidate._build_user_message(prompt,current_frame)],
                tools=candidate._tools(state_path),preserve_recent=1)
            context_hash=hashlib.sha256(json.dumps(messages,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        except Exception as exc:
            t.pending=None
            self._vir_emit('construction_failed',attempt_id=attempt_id,error_type=type(exc).__name__,
                           original_context_retained=True,request_sent=False)
            return None
        self._history_messages=[]
        self._summarized_knowledge=candidate._summarized_knowledge
        self._combined_register(VIR,attempt_id,messages)
        t.pending=None
        self._vir_emit('context_applied',attempt_id=attempt_id,context_sha256=context_hash,
                       cleared=['conversation','captured_reasoning','current_plan'],
                       preserved=['world_model','goal_model','action_model','recent_findings','open_questions','cross_level_notes'],
                       request_sent=False,environment_mutated=False)
        return {'prompt':prompt,'messages':messages}


    def _combined_reset(self):
        self._recovery_boundary_used=False
        self._k1_pending=None;self._k1_latest=None;self._context_generation=0
        self._mechanism_counts={};self._recovery_order=[];self._attempt_order=[];self._recovery_applications=[]

    def _k1_invalidate(self,reason):
        if self._k1_pending:
            self._vir_emit('expired',mechanism=K1,response_id=self._k1_pending['response_id'],reason=reason)
        self._k1_pending=None;self._k1_latest=None

    def _combined_record_attempt(self,mechanism,attempt_id):
        self._attempt_order.append({'mechanism':mechanism,'attempt_id':attempt_id,
            'action_ordinal':self._vir_tracker.ordinal,'turn_sequence':getattr(self,'_study2_turn_sequence',None),
            'order':len(self._attempt_order)+1})

    def _combined_register(self,mechanism,attempt_id,messages):
        self._k1_invalidate('context_rebuilt')
        self._context_generation+=1
        application={'id':attempt_id,'mechanism':mechanism,'response_received':False,'action_observed':False,
            'transport_ended':False,'prepared_message_hashes':[grid_hash(m) for m in messages]}
        self._recovery_order.append({'mechanism':mechanism,'attempt_id':attempt_id,
            'action_ordinal':self._vir_tracker.ordinal,'order':len(self._recovery_order)+1})
        self._recovery_applications.append(application);self._vir_applied=application

    def _combined_begin_entry(self,state_path,action_num,current_frame,history_entries,valid_actions,should_stop,k1_addendum):
        self._recovery_boundary_used=False;self._k1_addendum=k1_addendum
        if not self._combined_enabled:return None
        t=self._vir_tracker
        if t and t.pending and self._k1_pending and not t.attempted:
            self._vir_emit('arbitration',mechanism='COMBINED',conditions=[K1,VIR],selected=VIR,
                           K1_response_id=self._k1_pending['response_id'])
        prepared=self._vir_prepare_entry(state_path,action_num,current_frame,history_entries,valid_actions,should_stop)
        if self._recovery_boundary_used:return prepared
        if self._k1_pending:
            return self._k1_prepare(state_path,action_num,current_frame,history_entries,valid_actions,should_stop)
        return None

    def _combined_consider_k1(self,qualifies,eligible,response_id,request_id):
        if self._stagnation_recovery_threshold!=1:return eligible
        if not qualifies:
            self._k1_invalidate('nonqualifying_response');return False
        if not eligible:return False
        t=self._vir_tracker
        if t is None:return False
        self._k1_latest=(getattr(self,'_study2_turn_sequence',None),response_id)
        self._k1_pending={'response_id':response_id,'request_id':request_id,
                          'qualifying_turn_sequence':self._k1_latest[0],'ordinal':t.ordinal,
                          'level':t.level,'epoch':t.epoch,'generation':self._context_generation}
        self._vir_emit('eligible',mechanism=K1,response_id=response_id,request_id=request_id,
                       zero_semantic_tool_calls=True,zero_executed_environment_actions=True)
        if self._recovery_boundary_used:
            self._vir_emit('deferred',mechanism=K1,response_id=response_id,reason='one_attempt_per_analyze_entry')
            return False
        return True

    def _k1_prepare(self,state_path,action_num,current_frame,history_entries,valid_actions,should_stop):
        p=self._k1_pending;t=self._vir_tracker
        if self._stagnation_recovery_threshold!=1 or self._stagnation_recovery_used or self._recovery_boundary_used:return None
        if p is None or t is None:return None
        if should_stop is not None:
            try:
                if should_stop():return None
            except Exception:return None
        try:
            valid=(str(Path(state_path).resolve())==t.key and int(action_num)==t.ordinal==p['ordinal'] and
                current_frame is not None and int(current_frame.step)==t.ordinal and
                int(current_frame.level)==t.level==p['level'] and p['epoch']==t.epoch and
                p['generation']==self._context_generation and (p['qualifying_turn_sequence'],p['response_id'])==self._k1_latest)
        except Exception:valid=False
        if not valid:self._k1_invalidate('entry_revalidation');return None
        self._stagnation_recovery_used=True;self._no_tool_streak=0;self._recovery_boundary_used=True
        attempt_id=str(p['qualifying_turn_sequence'])+':'+str(p['response_id'])+':K1:attempt'
        self._combined_record_attempt(K1,attempt_id)
        self._vir_emit('attempt',mechanism=K1,attempt_id=attempt_id,response_id=p['response_id'],
                       qualifying_response_request_id=p['request_id'],qualifying_turn_sequence=p['qualifying_turn_sequence'])
        try:
            candidate=copy.copy(self)
            candidate._history_messages=copy.deepcopy(self._history_messages)
            candidate._summarized_knowledge=copy.deepcopy(self._summarized_knowledge)
            candidate._summarized_knowledge['current_plan']=''
            prompt=candidate._build_user_prompt(action_num,valid_actions=valid_actions,current_frame=current_frame,
                history_entries=history_entries,previous_step_summary=self._last_step_summary)
            prompt+='\n\n'+self._k1_addendum
            messages=candidate._trim_messages_for_context([
                {'role':'system','content':self._system_prompt},candidate._build_user_message(prompt,current_frame)],
                tools=candidate._tools(state_path),preserve_recent=1)
            context_hash=hashlib.sha256(json.dumps(messages,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        except Exception as exc:
            self._k1_pending=None
            self._vir_emit('construction_failed',mechanism=K1,attempt_id=attempt_id,error_type=type(exc).__name__,
                           original_context_retained=True,request_sent=False)
            return None
        self._history_messages=[];self._summarized_knowledge=candidate._summarized_knowledge
        self._combined_register(K1,attempt_id,messages)
        self._vir_emit('context_applied',mechanism=K1,attempt_id=attempt_id,context_sha256=context_hash,
                       cleared=['conversation','captured_reasoning','current_plan'],request_sent=False,
                       environment_mutated=False,gameplay_success_claimed=False)
        return {'prompt':prompt,'messages':messages}

    def _vir_before_request(self,request_id,messages):
        hashes=[grid_hash(m) for m in messages]
        for applied in self._recovery_applications:
            if applied['response_received'] or applied['transport_ended']:continue
            present=all(h in hashes for h in applied['prepared_message_hashes'])
            applied['request_id']=request_id
            applied['request_turn_sequence']=getattr(self,'_study2_turn_sequence',None)
            applied['prepared_context_present']=present
            self._vir_emit('next_request_attempt',mechanism=applied['mechanism'],attempt_id=applied['id'],
                request_id=request_id,transport_invocation=True,remote_acceptance_unverified=True,
                prepared_context_present=present,actual_messages_sha256=grid_hash(messages))
            if not present:
                applied['transport_ended']=True
                self._vir_emit('prepared_context_not_in_request',mechanism=applied['mechanism'],
                    attempt_id=applied['id'],request_id=request_id,request_exposed=False)

    def _vir_after_response(self,request_id):
        for applied in self._recovery_applications:
            if (not applied['response_received'] and not applied['transport_ended'] and
                applied.get('request_id')==request_id and applied.get('request_turn_sequence')==getattr(self,'_study2_turn_sequence',None)):
                applied['response_received']=True
                self._vir_emit('next_response',mechanism=applied['mechanism'],attempt_id=applied['id'],
                               request_id=request_id,request_exposed=True,prepared_context_present=True)

    def _vir_request_failed(self,request_id,error):
        for applied in self._recovery_applications:
            if not applied['response_received'] and not applied['transport_ended']:
                applied['transport_ended']=True
                self._vir_emit('next_request_failed',mechanism=applied['mechanism'],attempt_id=applied['id'],
                               request_id=request_id,error_type=type(error).__name__,request_exposure_unverified=True)

